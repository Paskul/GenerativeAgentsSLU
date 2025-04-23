import json
from datetime import timedelta
import tkinter.font as tkFont
from GenerativeAgents.llm.llm import generate_action_plan 
from GenerativeAgents.simulation.time_manager import TimeManager


class SimulationManager:

    def __init__(self, agents, environment, time_step=timedelta(minutes=10)):
        self.agents = agents
        self.environment = environment
        self.time_step = time_step
        self.time_manager = TimeManager()
        self.time_manager.time_step = self.time_step
        self.message_log: list[str] = ["Micro plans are reasoning …"]
        self.step_count: int = 0

    def add_message(self, text: str, speaker: str | None = None):
        """Append a line to the shared log (keep last 5 lines)."""
        line = f"{speaker}: {text}" if speaker else text
        self.message_log.append(line)
        if len(self.message_log) > 5:
            self.message_log.pop(0)

    def render_agents(self, canvas, tile_size: int):
        """Draw red dot + name for every agent (no speech bubbles)."""
        fnt = tkFont.Font(family="Courier New", size=8)
        canvas.delete("agent_layer")

        for ag in self.agents:
            cx = ag.x * tile_size + tile_size // 2
            cy = ag.y * tile_size + tile_size // 2
            r  = tile_size // 3
            canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                               fill="red", tags="agent_layer")
            canvas.create_text(cx, cy, text=ag.name,
                               fill="white", font=fnt, tags="agent_layer")

    def step(self):
        for agent in self.agents:
            plan_json = generate_action_plan(
                self.time_manager.current_time,   
                self.environment,                 
                agent
            )

            try:
                step_response = json.loads(plan_json)
            except json.JSONDecodeError:
                self.add_message("LLM JSON error; skipping " + agent.name)
                continue

           
            direction = step_response.get("direction")
            if direction == "up":
                agent.y = max(0, agent.y - 1)
            elif direction == "down":
                agent.y = min(self.environment.height - 1, agent.y + 1)
            elif direction == "left":
                agent.x = max(0, agent.x - 1)
            elif direction == "right":
                agent.x = min(self.environment.width - 1, agent.x + 1)

            if step_response.get("speech"):
                speech  = step_response["speech"]
                speaker = None if self.step_count == 0 else agent.name
                self.add_message(speech, agent.name)
            
        self.time_manager.advance()
        self.step_count += 1

    @staticmethod
    def clean_llm_output(text):
        text = text.strip()
        if text.startswith("```") and text.endswith("```"):
            text = text.strip("`")
            if text.lower().startswith("json"):
                text = text[4:].strip()
        return text

    def update_daily_plans(self, current_time):
        env_summary = (self.environment.get_layout_summary()
                       if hasattr(self.environment, "get_layout_summary")
                       else f"Grid of size {self.environment.width}x{self.environment.height} with designated features.")
        for agent in self.agents:
            if (not hasattr(agent, "daily_plan_date")) or (agent.daily_plan_date != current_time.date()):
                daily_plan_str = generate_daily_action_plan(current_time.strftime("%Y-%m-%d"), env_summary, agent, getattr(agent, "daily_plan", ""))
                if daily_plan_str:
                    cleaned_daily_plan = self.clean_llm_output(daily_plan_str)
                    try:
                        plan = json.loads(cleaned_daily_plan)
                        agent.daily_plan = plan.get("daily_plan", "")
                        agent.daily_plan_date = current_time.date()
                        print(f"New daily plan for {agent.name}: {agent.daily_plan}")
                    except Exception as e:
                        print(f"Error parsing daily plan output for {agent.name}: {e}")

    def update_agent(self, agent, current_time):
        print(f"[{current_time.strftime('%H:%M')}] Updating {agent.name}...")
        sim_time_str = current_time.strftime("%H:%M")
        vision = agent.get_visible_entities(self.environment, self.agents)
        prev_plan = getattr(agent, "prev_action_plan", "")
        action_plan_str = generate_action_plan(sim_time_str, vision, agent, prev_plan)
        if action_plan_str:
            cleaned_output = self.clean_llm_output(action_plan_str)
            try:
                plan = json.loads(cleaned_output)
                direction = plan.get("direction", None)
                speech = plan.get("speech", "")  
                
                new_x, new_y = agent.x, agent.y
                if direction == "up":
                    new_y += 1
                elif direction == "down":
                    new_y -= 1
                elif direction == "left":
                    new_x -= 1
                elif direction == "right":
                    new_x += 1

                if 0 <= new_x < self.environment.width and 0 <= new_y < self.environment.height:
                    if direction in ["up", "down", "left", "right"]:
                        agent.move(direction)
                        agent.prev_action_plan = cleaned_output
                        agent.speech = speech 
                        print(f"{agent.name} says: {speech}")
                    else:
                        print(f"Invalid direction received for {agent.name}: {direction}")
                else:
                    feedback = (f"ILLEGAL MOVE: Attempted to move {direction} from ({agent.x}, {agent.y}) "
                                f"to ({new_x}, {new_y}). Please follow the rules and do not move out of bounds. "
                                f"Previous position was ({agent.x}, {agent.y}).")
                    print(feedback)
                    agent.prev_action_plan = feedback

                if agent.speech:
                    speech_lower = agent.speech.lower()
                    for other in self.agents:
                        if other is not agent:
                            if other.name.lower() in speech_lower:
                                agent.update_relationship(other, 5)
            except Exception as e:
                print(f"Error parsing LLM output for {agent.name}: {e}")

    def render_agents(self, canvas, tile_size):
        font_obj = tkFont.Font(family="Courier New", size=10)
        for agent in self.agents:
            x_pixel = agent.x * tile_size
            y_pixel = agent.y * tile_size
            radius = tile_size // 3
            canvas.create_oval(
                x_pixel + tile_size/2 - radius,
                y_pixel + tile_size/2 - radius,
                x_pixel + tile_size/2 + radius,
                y_pixel + tile_size/2 + radius,
                fill="red",
                tags="agent_layer"
            )
            canvas.create_text(
                x_pixel + tile_size/2,
                y_pixel + tile_size/2,
                text=agent.name,
                fill="white",
                font=("Courier New", 8),
                tags="agent_layer"
            )
            if hasattr(agent, "speech") and agent.speech.strip() != "":
                speech_text = agent.speech.strip()
                bubble_padding = 4
                text_width = font_obj.measure(speech_text)
                text_height = font_obj.metrics("linespace")
                bubble_width = text_width + 2 * bubble_padding
                bubble_height = text_height + 2 * bubble_padding
                bubble_x = x_pixel + tile_size
                bubble_y = y_pixel + (tile_size - bubble_height) / 2
                canvas.create_rectangle(
                    bubble_x, bubble_y,
                    bubble_x + bubble_width, bubble_y + bubble_height,
                    fill="white", outline="black", tags="agent_layer"
                )
                canvas.create_text(
                    bubble_x + bubble_width / 2,
                    bubble_y + bubble_height / 2,
                    text=speech_text,
                    fill="black",
                    font=("Courier New", 10),
                    tags="agent_layer"
                )

    def add_message(self, text, speaker=None):
        line = f"{speaker}: {text}" if speaker else text
        self.message_log.append(line)
        if len(self.message_log) > 5:
            self.message_log.pop(0)

    def run(self, max_steps=None):
        while self.active:
            self.step()
            if max_steps is not None and self.step_count >= max_steps:
                self.active = False
            time.sleep(0.5)
