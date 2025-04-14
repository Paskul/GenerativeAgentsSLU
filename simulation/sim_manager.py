import time
import json
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
import tkinter.font as tkFont
from GenerativeAgents.agents.agent import Agent
from GenerativeAgents.environment.map import Map
from GenerativeAgents.simulation.time_manager import TimeManager
from GenerativeAgents.llm.llm import generate_action_plan, generate_daily_action_plan

class SimulationManager:
    def __init__(self, agents, environment, start_time=None, time_step=timedelta(minutes=1)):
        self.agents = agents            # Manager holds the agents.
        self.environment = environment  # The map environment.
        self.time_manager = TimeManager(start_time=start_time, time_step=time_step)
        self.active = True
        self.step_count = 0

        # Initialize relationships for all agents: every other agent starts at 0.
        for agent in self.agents:
            for other in self.agents:
                if other is not agent:
                    if other.name not in agent.relationships:
                        agent.relationships[other.name] = 0

    def step(self):
        current_time = self.time_manager.advance()
        self.step_count += 1

        # Update daily plans at the start of a new day.
        self.update_daily_plans(current_time)

        # Use ThreadPoolExecutor to update each agent concurrently.
        with ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
            futures = [executor.submit(self.update_agent, agent, current_time)
                       for agent in self.agents]
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print("Error updating an agent:", e)

    @staticmethod
    def clean_llm_output(text):
        text = text.strip()
        if text.startswith("```") and text.endswith("```"):
            text = text.strip("`")
            if text.lower().startswith("json"):
                text = text[4:].strip()
        return text

    def update_daily_plans(self, current_time):
        # Obtain a summary of the environment layout.
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
                speech = plan.get("speech", "")  # New field: the generated one-sentence speech.
                
                # Compute new coordinates based on the intended move.
                new_x, new_y = agent.x, agent.y
                if direction == "up":
                    new_y += 1
                elif direction == "down":
                    new_y -= 1
                elif direction == "left":
                    new_x -= 1
                elif direction == "right":
                    new_x += 1

                # Check if the move is within bounds.
                if 0 <= new_x < self.environment.width and 0 <= new_y < self.environment.height:
                    if direction in ["up", "down", "left", "right"]:
                        agent.move(direction)
                        agent.prev_action_plan = cleaned_output
                        agent.speech = speech  # Store new speech.
                        print(f"{agent.name} says: {speech}")
                    else:
                        print(f"Invalid direction received for {agent.name}: {direction}")
                else:
                    # Illegal move attempt: provide feedback.
                    feedback = (f"ILLEGAL MOVE: Attempted to move {direction} from ({agent.x}, {agent.y}) "
                                f"to ({new_x}, {new_y}). Please follow the rules and do not move out of bounds. "
                                f"Previous position was ({agent.x}, {agent.y}).")
                    print(feedback)
                    agent.prev_action_plan = feedback

                # Relationship update based on speech:
                # Scan the agent's speech for mentions of other agents' names.
                if agent.speech:
                    speech_lower = agent.speech.lower()
                    for other in self.agents:
                        if other is not agent:
                            if other.name.lower() in speech_lower:
                                # Update relationship: add 5 points.
                                agent.update_relationship(other, 5)
            except Exception as e:
                print(f"Error parsing LLM output for {agent.name}: {e}")

    def render_agents(self, canvas, tile_size):
        # Create a Font object to measure text dimensions.
        font_obj = tkFont.Font(family="Arial", size=10)
        for agent in self.agents:
            x_pixel = agent.x * tile_size
            y_pixel = agent.y * tile_size
            radius = tile_size // 3
            # Draw agent marker (red circle) and name.
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
                font=("Arial", 8),
                tags="agent_layer"
            )
            # Draw the speech bubble if the agent has non-empty speech.
            if hasattr(agent, "speech") and agent.speech.strip() != "":
                speech_text = agent.speech.strip()
                bubble_padding = 4
                # Calculate text dimensions.
                text_width = font_obj.measure(speech_text)
                text_height = font_obj.metrics("linespace")
                bubble_width = text_width + 2 * bubble_padding
                bubble_height = text_height + 2 * bubble_padding
                # Position the bubble to the right of the agent.
                bubble_x = x_pixel + tile_size
                bubble_y = y_pixel + (tile_size - bubble_height) / 2
                # Draw bubble background.
                canvas.create_rectangle(
                    bubble_x, bubble_y,
                    bubble_x + bubble_width, bubble_y + bubble_height,
                    fill="white", outline="black", tags="agent_layer"
                )
                # Draw speech text centered in the bubble.
                canvas.create_text(
                    bubble_x + bubble_width / 2,
                    bubble_y + bubble_height / 2,
                    text=speech_text,
                    fill="black",
                    font=("Arial", 10),
                    tags="agent_layer"
                )

    def run(self, max_steps=None):
        while self.active:
            self.step()
            if max_steps is not None and self.step_count >= max_steps:
                self.active = False
            time.sleep(0.5)
