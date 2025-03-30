import time
from typing import List, Optional
from datetime import timedelta

from agent.agent import Agent
from map.map import Map
import TimeManager

class SimulationManager:
    def __init__(
        self,
        agents: List[Agent],
        environment: Map,
        start_time=None,
        time_step: timedelta = timedelta(minutes=1),
    ):
        self.agents = agents
        self.environment = environment

        # to handle simulation time
        self.time_manager = TimeManager(start_time=start_time, time_step=time_step)

        self.active = True
        self.step_count = 0


    def step(self) -> None:
        # ADVANCE ENTIRE SIM BY 1 STEP
        current_time = self.time_manager.advance()
        self.step_count += 1

        for agent in self.agents:
            self.update_agent(agent, current_time)

        # if we change Map over time, can do it here

    def update_agent(self, agent: Agent, current_time):
        # SHOULD determine and apply the agent's next action.

        print(f"[{current_time.strftime('%H:%M')}] Updating {agent.name}...")

        # Example: move the agent "up". Replace with actual.
        agent.move("up")


    def run(self, max_steps: Optional[int] = None):
        # simulation loop until a maximum step count is reached or it is manually stopped.
        while self.active:
            self.step()
            if max_steps is not None and self.step_count >= max_steps:
                self.active = False

            # real-time delay to throttle the simulation loop.
            # we have to test this in actual
            time.sleep(0.5)
