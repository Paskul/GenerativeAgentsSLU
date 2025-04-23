import tkinter as tk
from tkinter import messagebox, filedialog
from GenerativeAgents.ui.simulation_screen import run_simulation

def show_help():
    messagebox.showinfo(
        "Help",
        "How to operate the simulation:\n\n"
        "- Click 'New Simulation' to start a fresh simulation.\n"
        "- Click 'Load Simulation' to load a saved simulation.\n\n"
        "Agents plan and act autonomously using graphical assets."
    )

def exit_application(root):
    root.quit()

def load_simulation():
    filepath = filedialog.askopenfilename(
        title="Select a Simulation to Load",
        filetypes=[("Simulation Files", "*.sim")]
    )
    if filepath:
        messagebox.showinfo("Load Simulation", f"Loaded simulation from: {filepath}")
    else:
        messagebox.showwarning("Load Simulation", "No simulation selected!")

def toggle_full_screen(root, is_full_screen):
    is_full_screen = not is_full_screen
    root.attributes("-fullscreen", is_full_screen)
    if not is_full_screen:
        root.geometry("800x600")
    else:
        root.geometry("")
    return is_full_screen

def update_help_button_position(root, help_button):
    window_width = root.winfo_width()
    help_button.place(x=window_width - help_button.winfo_width() - 10, y=10)

def run_initial_screen():
    root = tk.Tk()
    root.title("Generative Agents Simulation - Main Menu")
    root.geometry("800x600")
    root.minsize(800, 600)
    is_full_screen = False

    root.bind("<F11>", lambda event: toggle_full_screen(root, is_full_screen))
    
    frame = tk.Frame(root)
    frame.pack(side="top", pady=60)
    
    exit_button = tk.Button(root, text="Exit", command=lambda: exit_application(root), font=('Courier New', 10))
    exit_button.place(x=10, y=10)
    
    help_button = tk.Button(root, text="?", command=show_help, font=('Courier New', 14), width=2, height=1)
    help_button.place(x=root.winfo_width() - help_button.winfo_width() - 10, y=10)
    
    new_sim_button = tk.Button(
        frame,
        text="New Simulation",
        command=lambda: (root.destroy(), run_simulation()),
        font=('Courier New', 14),
        width=20,
        height=2
    )
    new_sim_button.grid(row=0, column=0, padx=10, pady=10)
    
    load_sim_button = tk.Button(
        frame,
        text="Load Simulation",
        command=load_simulation,
        font=('Courier New', 14),
        width=20,
        height=2
    )
    load_sim_button.grid(row=1, column=0, padx=10, pady=10)
    
    root.bind("<Configure>", lambda event: update_help_button_position(root, help_button))
    
    root.mainloop()

if __name__ == "__main__":
    run_initial_screen()
