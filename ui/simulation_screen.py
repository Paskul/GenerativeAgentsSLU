import tkinter as tk
import tkinter.font as tkFont
import textwrap
import time
from datetime import timedelta
from threading import Thread

from GenerativeAgents.environment.map import Map
from GenerativeAgents.simulation.sim_manager import SimulationManager
from GenerativeAgents.agents.agent import Agent

def run_simulation():
    sim_root = tk.Tk()
    sim_root.title("Generative Agents Simulation - Map")
    sim_root.geometry("1536x864") 

    tile_size = 32
    map_width = 48
    map_height = 27

    canvas = tk.Canvas(
        sim_root,
        width=map_width * tile_size,
        height=map_height * tile_size,
        bd=0,
        highlightthickness=0
    )
    canvas.pack(fill=tk.BOTH, expand=True)

    my_map = Map(width=map_width, height=map_height)
    my_map.render_map(canvas, tile_size=tile_size)

    agent_sprites = {}
    assets_dir = "/Users/avaenke/Desktop/GenerativeAgents/assets"
    for name in ("Ada","Gus","Clara","Otto","Alan","Olive","Mavis","Finn"):
        try:
            img = tk.PhotoImage(file=f"{assets_dir}/{name}.png")
            ow, oh = img.width(), img.height()
            sx = max(1, ow // tile_size)
            sy = max(1, oh // tile_size)
            if sx>1 or sy>1:
                img = img.subsample(sx, sy)
            agent_sprites[name] = img
        except tk.TclError:
            agent_sprites[name] = None

    all_agents = [
        Agent("Ada",   "Farmer",    29, "Smart",      2,  2),
        Agent("Gus",   "Fisherman", 32, "Shy",        5,  5),
        Agent("Clara", "Shop Owner",40, "Friendly",   8,  2),
        Agent("Otto",  "Shop Owner", 4, "Persuasive", 10, 6),
        Agent("Alan",  "Farmer",    57, "Grumpy",     14, 4),
        Agent("Olive", "Artisan",   30, "Creative",   17, 8),
        Agent("Mavis", "Farmer",    25, "Bubbly",     20,10),
        Agent("Finn",  "Student",    9, "Hyper",      24,12)
    ]

    selected_agents = all_agents[:8]

    sim_manager = SimulationManager(
        agents=selected_agents,
        environment=my_map,
        time_step=timedelta(minutes=10)
    )
    sim_manager.message_log.append("Waiting for agents to generate their action plans…")

    def update_ui():
        canvas.delete("agent_layer")
        for agent in sim_manager.agents:
            cx = agent.x * tile_size + tile_size//2
            cy = agent.y * tile_size + tile_size//2
            sprite = agent_sprites.get(agent.name)
            if sprite:
                canvas.create_image(cx, cy, image=sprite, tags="agent_layer")
            else:
                r = tile_size // 3
                canvas.create_oval(
                    cx - r, cy - r, cx + r, cy + r,
                    fill="red", tags="agent_layer"
                )
            canvas.create_text(
                cx, cy + tile_size//2 + 5,
                text=agent.name,
                fill="white",
                font=("Arial", 8),
                tags="agent_layer"
            )

        canvas.delete("clock_layer")
        clock_text = sim_manager.time_manager.current_time.strftime("%H:%M")
        canvas.create_text(
            1470, 820,
            text=clock_text,
            fill="black",
            font=("Arial", 24, "bold"),
            tags="clock_layer"
        )

        canvas.delete("speech_log_layer")
        log_x, log_y = 900, 550
        box_w, box_h = 600, 250
        padding = 10
        canvas.create_rectangle(
            log_x, log_y,
            log_x + box_w, log_y + box_h,
            fill="white", outline="black", width=2,
            tags="speech_log_layer"
        )
        bold_font   = tkFont.Font(family="Arial", size=12, weight="bold")
        normal_font = tkFont.Font(family="Arial", size=12)
        line_h      = 20
        wrap_px     = box_w - 2 * padding
        char_wrap   = max(20, int(wrap_px / normal_font.measure("M")))
        y_cursor    = log_y + padding

        for full_msg in sim_manager.message_log:
            if ":" in full_msg:
                name, speech = full_msg.split(":", 1)
                name_text = name + ":"
            else:
                name_text, speech = "", full_msg

            wrapped = textwrap.wrap(speech.strip(), width=char_wrap)
            name_w = bold_font.measure(name_text + " ")

            for idx, line in enumerate(wrapped):
                if idx == 0 and name_text:
                    canvas.create_text(
                        log_x + padding, y_cursor,
                        anchor="nw", text=name_text,
                        font=bold_font, fill="black",
                        tags="speech_log_layer"
                    )
                    canvas.create_text(
                        log_x + padding + name_w, y_cursor,
                        anchor="nw", text=line,
                        font=normal_font, fill="black",
                        width=wrap_px - name_w,
                        tags="speech_log_layer"
                    )
                else:
                    canvas.create_text(
                        log_x + padding + name_w, y_cursor,
                        anchor="nw", text=line,
                        font=normal_font, fill="black",
                        width=wrap_px - name_w,
                        tags="speech_log_layer"
                    )
                y_cursor += line_h

            y_cursor += line_h//2
            if y_cursor > log_y + box_h - padding:
                break

    update_ui()

    def simulation_loop():
        sim_manager.step()
        sim_root.after(0, update_ui)

    def run_steps():
        while True:
            simulation_loop()
            time.sleep(0.5)

    Thread(target=run_steps, daemon=True).start()
    sim_root.mainloop()


if __name__ == "__main__":
    run_simulation()
