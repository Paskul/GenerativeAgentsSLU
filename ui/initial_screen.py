# ui/initial_screen.py

import os
import tkinter as tk
from tkinter import messagebox
from GenerativeAgents.ui.simulation_screen import run_simulation, agent_specs

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")


def show_help():
    win = tk.Toplevel()
    win.title("Help & Agents Info")
    win.geometry("500x600")

    # Create canvas + scrollbar for scrolling content
    canvas = tk.Canvas(win, borderwidth=0)
    scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas)
    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ——— Original Help Text ————————————————————————————————
    help_text = (
        "How to operate the simulation:\n\n"
        "- Click 'New Simulation' to start a fresh simulation.\n\n"
        "- Once in the simulation, agents will plan and act autonomously.\n\n"
        "- For 'overseer' plans, type what is desired in the textbox, see agents react.\n\n"
        "- Above the textbox, agent dialouge and thoughts are shown.\n\n"
        "Below is a list of all agents in this world:\n"
    )
    tk.Label(
        scroll_frame,
        text=help_text,
        font=("Pixellari", 12),
        anchor="w",
        justify="left",
        wraplength=360
    ).pack(fill="x", padx=10, pady=(10, 20))

    # ——— Agent Portraits + Descriptions ————————————————————————
    for name, role, age, pers, *_ in agent_specs:
        row = tk.Frame(scroll_frame, pady=5)
        row.pack(fill="x", padx=10)

        img_path = os.path.join(ASSETS_DIR, f"{name}.png")
        try:
            photo = tk.PhotoImage(file=img_path)
            ow, oh = photo.width(), photo.height()
            factor = max(1, ow // 64, oh // 64)
            if factor > 1:
                photo = photo.subsample(factor, factor)
        except Exception:
            photo = None

        if photo:
            lbl_img = tk.Label(row, image=photo)
            lbl_img.image = photo
            lbl_img.pack(side="left", padx=(0,10))

        desc = f"{name}: {role}, Age {age}, Personality: {pers}"
        tk.Label(
            row,
            text=desc,
            font=("Pixellari", 12),
            anchor="w",
            justify="left",
            wraplength=300
        ).pack(side="left", fill="x")

    win.transient(root)   # keep on top of main
    win.grab_set()        # block interaction until closed


def exit_application(root):
    root.quit()


def toggle_full_screen(root, is_full):
    is_full = not is_full
    root.attributes("-fullscreen", is_full)
    return is_full


def update_help_button_position(root, btn):
    w = root.winfo_width()
    btn.place(x=w - btn.winfo_reqwidth() - 10, y=10)


def run_initial_screen():
    global root
    root = tk.Tk()
    root.title("Generative Agents Simulation - Main Menu")

    # ——— Load + size to background.png —————————————————————————
    bg_path = os.path.join(ASSETS_DIR, "background.png")
    try:
        bg_img = tk.PhotoImage(file=bg_path)
        w, h = bg_img.width(), bg_img.height()
        root.geometry(f"{w}x{h}")
        root.resizable(False, False)
        lbl = tk.Label(root, image=bg_img)
        lbl.image = bg_img
        lbl.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print("Warning loading background:", e)
        root.geometry("800x600")

    # ——— Fullscreen toggle ——————————————————————————————————
    is_full = False
    root.bind("<F11>", lambda e: toggle_full_screen(root, is_full))

    # ——— Exit button —————————————————————————————————————
    exit_btn = tk.Button(
        root, text="Exit",
        command=lambda: exit_application(root),
        font=("Pixellari", 10),
        width=6, height=1
    )
    exit_btn.place(x=10, y=10)

    # ——— Help button —————————————————————————————————————
    help_btn = tk.Button(
        root, text="?",
        command=show_help,
        font=("Pixellari", 14),
        width=2, height=1
    )
    help_btn.place(x=root.winfo_width()-help_btn.winfo_reqwidth()-10, y=10)
    root.bind("<Configure>", lambda e: update_help_button_position(root, help_btn))

    # ——— New Simulation button ————————————————————————————
    frame = tk.Frame(root, highlightthickness=0)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    new_btn = tk.Button(
        frame,
        text="New Simulation",
        command=lambda: (root.destroy(), run_simulation()),
        font=("Pixellari", 14),
        width=20, height=2
    )
    new_btn.pack()

    root.mainloop()


if __name__ == "__main__":
    run_initial_screen()
