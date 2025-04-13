import time
import json
from datetime import timedelta
import tkinter as tk
from GenerativeAgents.agents.agent import Agent
from GenerativeAgents.environment.map import Map
from GenerativeAgents.simulation.time_manager import TimeManager
from GenerativeAgents.llm.llm import generate_action_plan  # Import the new LLM function

class SimulationManager:
    def __init__(self, agents, environment, start_time=None, time_step=timedelta(minutes=1)):
        self.agents = agents            # Manager holds the agents
        self.environment = environment
        self.time_manager = TimeManager(start_time=start_time, time_step=time_step)
        self.active = True
        self.step_count = 0

    def step(self):
        current_time = self.time_manager.advance()
        self.step_count += 1

        for agent in self.agents:
            self.update_agent(agent, current_time)

    @staticmethod
    def clean_llm_output(text):
        """
        Remove markdown code block formatting (e.g. triple backticks and language hints)
        from the LLM output so that the result can be parsed as valid JSON.
        """
        text = text.strip()
        if text.startswith("```") and text.endswith("```"):
            text = text.strip("`")
            if text.lower().startswith("json"):
                text = text[4:].strip()
        return text

    def update_agent(self, agent, current_time):
        print(f"[{current_time.strftime('%H:%M')}] Updating {agent.name}...")
        sim_time_str = current_time.strftime("%H:%M")
        vision = agent.get_visible_entities(self.environment, self.agents)
        prev_plan = getattr(agent, "prev_action_plan", "")
        action_plan_str = generate_action_plan(sim_time_str, vision, agent, prev_plan)
        if action_plan_str:
            # Clean the output before parsing
            cleaned_output = self.clean_llm_output(action_plan_str)
            try:
                plan = json.loads(cleaned_output)
                direction = plan.get("direction", None)
                if direction in ["up", "down", "left", "right"]:
                    agent.move(direction)
                    agent.prev_action_plan = cleaned_output
                else:
                    print(f"Invalid direction received for {agent.name}: {direction}")
            except Exception as e:
                print(f"Error parsing LLM output for {agent.name}: {e}")

    def render_agents(self, canvas, tile_size):
        """
        Render all agents onto the canvas.
        Each agent is drawn with a red circle and their name, using the tag "agent_layer".
        """
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
                font=("Arial", 8),
                tags="agent_layer"
            )

    def render_overlay(self, canvas):
        def on_exit():
            self.active = False  # Stop the simulation loop
            canvas.master.destroy()  # Close the window
            # Create Exit button and place it in the top-right
        exit_button = tk.Button(canvas.master, text="Exit", command=on_exit, bg="red", fg="white")
        exit_button.place(x=10,y=10)
        
    def run(self, max_steps=None):
        while self.active:
            self.step()
            if max_steps is not None and self.step_count >= max_steps:
                self.active = False
            time.sleep(0.5)
