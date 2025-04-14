import tkinter as tk
import time
from datetime import timedelta
from threading import Thread
from GenerativeAgents.environment.map import Map
from GenerativeAgents.simulation.sim_manager import SimulationManager
from GenerativeAgents.agents.agent import Agent

def run_simulation():
    sim_root = tk.Tk()
    sim_root.title("Generative Agents Simulation - Map")
    sim_root.geometry("1536x864")  # 48 tiles x 32px = 1536; 27 tiles x 32px = 864

    # Map dimensions and tile size.
    tile_size = 32
    map_width = 48
    map_height = 27

    # Create a canvas with no borders.
    canvas = tk.Canvas(sim_root, width=map_width * tile_size, height=map_height * tile_size,
                       bd=0, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    # Create and render the base map (drawn only once).
    my_map = Map(width=map_width, height=map_height)
    my_map.render_map(canvas, tile_size=tile_size)

    # Create some agents.
    agents = [
        Agent("Ada", "Farmer", 29, "Smart", 2, 2),
        Agent("Gus", "Fisherman", 32, "Shy", 5, 5),
        Agent("Clara", "Shop Owner", 40, "Friendly", 8, 2),
        Agent("Otto", "Shop Owner", 4, "Persuasive", 10, 6),
        Agent("Olive", "Artisan", 30, "Creative", 17, 8),
    ]

    # Create the simulation manager with a timestep of 10 minutes.
    sim_manager = SimulationManager(agents=agents, environment=my_map, time_step=timedelta(minutes=10))

    # Flag to allow pausing if needed (optional).
    simulation_running = [True]

    def update_ui():
        """Update only the dynamic parts of the UI (agent layer and clock)."""
        canvas.delete("agent_layer")
        sim_manager.render_agents(canvas, tile_size=tile_size)
        canvas.delete("clock_layer")
        clock_text = sim_manager.time_manager.current_time.strftime("%H:%M")
        canvas.create_text(1470, 820, text=clock_text, fill="black",
                           font=("Arial", 24, "bold"), tags="clock_layer")

    def simulation_loop():
        """Run one simulation step in the background and then schedule UI update."""
        if simulation_running[0]:
            # Run a simulation step (this can block, but it's in a background thread).
            sim_manager.step()
        # Schedule the UI update on the main thread.
        sim_root.after(0, update_ui)

    def run_simulation_steps():
        """This function runs repeatedly in a background thread."""
        while True:
            simulation_loop()
            # Sleep for 500ms between simulation steps.
            # This sleep is in the background thread, so it doesn't block the GUI.
            time.sleep(0.5)

    # Start the simulation steps in a separate background thread.
    simulation_thread = Thread(target=run_simulation_steps, daemon=True)
    simulation_thread.start()

    sim_root.mainloop()

if __name__ == "__main__":
    run_simulation()
