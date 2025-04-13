import tkinter as tk
from GenerativeAgents.environment.map import Map
from GenerativeAgents.simulation.sim_manager import SimulationManager
from GenerativeAgents.agents.agent import Agent

def run_simulation():
    sim_root = tk.Tk()
    sim_root.title("Generative Agents Simulation - Map")
    sim_root.geometry("1536x864")  # 48 * 32 x 27 * 32

    # Map and tile dimensions
    tile_size = 32
    map_width = 48
    map_height = 27

    # Create the canvas (with no extra borders)
    canvas = tk.Canvas(sim_root, width=map_width * tile_size, height=map_height * tile_size, bd=0, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Create the base map and render it once.
    my_map = Map(width=map_width, height=map_height)
    my_map.render_map(canvas, tile_size=tile_size)

    # Create some agents.
    agents = [
        Agent(name="Alice", role="Farmer", age=30, personality="cheerful", x=5, y=5, vision_radius=5),
        Agent(name="Bob", role="Merchant", age=40, personality="curious", x=10, y=15, vision_radius=5)
    ]
    # Create the simulation manager holding the agents and map.
    sim_manager = SimulationManager(agents=agents, environment=my_map)

    def simulation_step():
        # Update simulation: for each agent, the LLM is called and the agent moves accordingly.
        sim_manager.step()
        # Update only the agent layer by deleting items with the "agent_layer" tag.
        canvas.delete("agent_layer")
        sim_manager.render_agents(canvas, tile_size=tile_size)
        # Schedule the next simulation step after all LLM calls are complete.
        sim_root.after(500, simulation_step)
        
    sim_root.after(1000, lambda: sim_manager.render_overlay(canvas))

    # Start the simulation loop.
    sim_root.after(500, simulation_step)
    sim_root.mainloop()

if __name__ == "__main__":
    run_simulation()
