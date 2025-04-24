# ui/simulation_screen.py
import os
import time
import textwrap
import tkinter as tk
import tkinter.font as tkFont
from datetime import timedelta
from threading import Thread

from GenerativeAgents.environment.map      import Map
from GenerativeAgents.simulation.sim_manager import SimulationManager
from GenerativeAgents.agents.agent         import Agent

# ---------------------------------------------------------------- main entry
def run_simulation() -> None:
    # ---------- window -------------------------------------------------------
    sim_root = tk.Tk()

    sim_root.title("Generative Agents Simulation – Map")
    tile_size = 32
    map_width, map_height = 48, 27
    window_w, window_h = map_width * tile_size, map_height * tile_size
    sim_root.geometry(f"{window_w}x{window_h}")

    # ---------- static canvas + map -----------------------------------------
    canvas = tk.Canvas(sim_root, width=window_w, height=window_h,
                       bd=0, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    game_map = Map(width=map_width, height=map_height)
    game_map.render_map(canvas, tile_size=tile_size)

    # ---------- agents ------------------------------------------------------
    agent_specs = [
        ("Ada",   "Farmer",    29, "Smart",      2,  2),
        ("Gus",   "Fisherman", 32, "Shy",        5,  5),
        ("Clara", "ShopOwner", 40, "Friendly",   8,  2),
        ("Otto",  "ShopOwner",  4, "Persuasive",10,  6),
        ("Alan",  "Farmer",    57, "Grumpy",    14,  4),
        ("Olive", "Artisan",   30, "Creative",  17,  8),
        ("Mavis", "Farmer",    25, "Bubbly",    20, 9),
        ("Finn",  "Student",    9, "Hyper",     24, 9)
    ]
    agents = [Agent(*spec, vision_radius=5) for spec in agent_specs]

    # ---------- sprite map --------------------------------------------------
    base_dir   = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "..", "assets")
    sprite_map: dict[str, tk.PhotoImage] = {}

    for name, *_ in agent_specs:
        p = os.path.join(assets_dir, f"{name}.png")
        try:
            img = tk.PhotoImage(file=p)
            # down-sample so it fits in one 32×32 tile
            sx = max(1, img.width()  // tile_size)
            sy = max(1, img.height() // tile_size)
            if sx > 1 or sy > 1:
                img = img.subsample(sx, sy)
            sprite_map[name] = img
        except Exception:
            sprite_map[name] = None

    # ---------- simulation manager ------------------------------------------
    sim_manager = SimulationManager(
        agents=agents,
        environment=game_map,
        time_step=timedelta(minutes=10)
    )

    # ---------- helper: pixel-accurate wrapper ------------------------------
    def wrap_pixel(text: str, max_px: int, font: tkFont.Font) -> list[str]:
        words, lines, cur = text.split(), [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if font.measure(trial) <= max_px:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines or [""]

    # ---------- UI update ----------------------------------------------------
    def update_ui() -> None:
        canvas.delete("agent_layer", "clock_layer", "speech_log_layer")

        # ---- agents & bubbles ---------------------------------------------------
        sim_manager.render_agents(canvas, tile_size, sprite_map)

        # ---- outlined clock (top-right) ----------------------------------------
        clock_txt = sim_manager.time_manager.current_time.strftime("%H:%M")
        clk_fnt   = tkFont.Font(family="Pixellari", size=24)
        cx, cy = window_w - 20, 20
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
            canvas.create_text(cx+dx, cy+dy, anchor="ne",
                            text=clock_txt, fill="black",
                            font=clk_fnt, tags="clock_layer")
        canvas.create_text(cx, cy, anchor="ne",
                        text=clock_txt, fill="white",
                        font=clk_fnt, tags="clock_layer")

        # ---- transparent speech area (lower-right) -----------------------------
        pad, line_gap, box_w = 10, 2, 640
        bold_fnt   = tkFont.Font(family="Pixellari", size=12, weight="bold")
        normal_fnt = tkFont.Font(family="Pixellari", size=12)
        wrap_px    = box_w - 2*pad
        line_h     = normal_fnt.metrics("linespace") + line_gap

        if sim_manager.daily_ready:
            raw_msgs = [(f"{a.name}:", a.speech.strip() or "…")
                        for a in sorted(sim_manager.agents,
                                        key=lambda a: a.name.lower())]
        else:
            raw_msgs = [("", "Generating daily plans …")]

        lines: list[tuple[str, str, int]] = []
        for lab, body in raw_msgs:
            name_px = bold_fnt.measure(lab + " ") if lab else 0
            for idx, seg in enumerate(
                wrap_pixel(body, wrap_px - name_px, normal_fnt)
            ):
                lines.append((lab if idx == 0 else "", seg, name_px))

        total_h = len(lines) * line_h + 2*pad
        input_h = 36                            # ≈ height of overseer entry box
        x0 = window_w - box_w - 10              # 10-px right margin
        y0 = window_h - input_h - total_h  # 0-px gap above entry box ( -x appended if x was px gap)
        y  = y0 + pad

        def draw_outlined(tx, ty, text, font, fg="white"):
            for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                canvas.create_text(tx+dx, ty+dy, anchor="nw",
                                text=text, font=font, fill="black",
                                tags="speech_log_layer")
            canvas.create_text(tx, ty, anchor="nw",
                            text=text, font=font, fill=fg,
                            width=wrap_px, tags="speech_log_layer")

        for lab, seg, n_px in lines:
            if lab:
                draw_outlined(x0+pad,        y, lab, bold_fnt)
            draw_outlined(x0+pad+n_px, y, seg, normal_fnt)
            y += line_h

    # ---------- background simulation thread ---------------------------------
    def sim_loop() -> None:
        while True:
            sim_manager.step()
            sim_root.after(0, update_ui)
            time.sleep(0.5)

    Thread(target=sim_loop, daemon=True).start()
    update_ui()

    # ---------- overseer input box -------------------------------------------
    input_frame = tk.Frame(sim_root)
    input_frame.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")  # 10-px margin

    cmd_var = tk.StringVar()
    entry = tk.Entry(input_frame, textvariable=cmd_var,
                    font=("Pixellari", 12), width=63)
    entry.pack(side="left")

    def send_cmd(_=None):
        txt = cmd_var.get().strip()
        if txt:
            sim_manager.add_directive(txt)
            cmd_var.set("")

    tk.Button(input_frame, text="Send",
            font=("Pixellari", 12), command=send_cmd).pack(side="left", padx=4)
    entry.bind("<Return>", send_cmd)

    # -------------------------------------------------------------------------
    sim_root.mainloop()


# ---------------------------------------------------------------- stand-alone
if __name__ == "__main__":
    run_simulation()
