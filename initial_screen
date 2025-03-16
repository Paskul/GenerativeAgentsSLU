import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# Function to handle the Help button click
def show_help():
    messagebox.showinfo("Help", 
                        "How to operate the simulation:\n\n"
                        "- Click 'New Simulation' to start a fresh simulation.\n"
                        "- Click 'Load Simulation' to load a saved simulation.\n"
                        "- Enter custom prompts to influence the simulation.\n"
                        "How Generative Agents Work:\n\n"
                        "- Agents plan and act autonomously based on your input.\n"
                        "- They interact with the world and other agents.\n"
                        "Suggestions:\n\n"
                        "- Start with a new simulation and observe agent behavior.")

# Function to handle the Exit button click
def exit_application():
    root.quit()

# Function to handle the New Simulation button click
def new_simulation():
    messagebox.showinfo("New Simulation", "Starting a new simulation...")

# Function to handle the Load Simulation button click
def load_simulation():
    filepath = filedialog.askopenfilename(title="Select a Simulation to Load", filetypes=[("Simulation Files", "*.sim")])
    if filepath:
        messagebox.showinfo("Load Simulation", f"Loaded simulation from: {filepath}")
    else:
        messagebox.showwarning("Load Simulation", "No simulation selected!")

# Function to toggle full-screen mode
def toggle_full_screen(event=None):
    global is_full_screen
    is_full_screen = not is_full_screen
    root.attributes("-fullscreen", is_full_screen)
    if not is_full_screen:
        root.geometry("800x600")  # Set to default window size if exiting full-screen
    else:
        root.geometry("")  # Set to full-screen

# Function to update the position of the Help button (top-right corner)
def update_help_button_position():
    window_width = root.winfo_width()
    help_button.place(x=window_width - help_button.winfo_width() - 10, y=10)

# Function to update the scene (pine trees and house) on window resize
def update_scene(event=None):
    # Clear the canvas before redrawing
    canvas.delete("all")
    
    # Get current window size
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Calculate relative positions and sizes based on window size
    tree_width = window_width // 12  # Example: Adjust tree width based on window size
    tree_height = window_height // 4  # Adjust tree height based on window size
    
    house_width = window_width // 5  # Adjust house width based on window size
    house_height = window_height // 3  # Adjust house height based on window size

    # Bring trees and house closer to top by reducing vertical offset
    tree_y_offset = window_height // 10  # Further moving trees up
    house_y_offset = window_height // 6  # Moving house up closer to the top

    # Drawing pine trees dynamically based on window size
    # Tree 1 (left)
    canvas.create_polygon(window_width // 15 + tree_width // 2, tree_y_offset,  # Top point of the triangle
                          window_width // 15 - tree_width, tree_y_offset + tree_height,  # Left point
                          window_width // 15 + tree_width * 2, tree_y_offset + tree_height,  # Right point
                          fill='darkgreen')  # Pine foliage

    # Tree trunk 1
    canvas.create_rectangle(window_width // 15 + tree_width, tree_y_offset + tree_height,
                             window_width // 15 + tree_width + 10, tree_y_offset + tree_height + 30, fill='brown')  # Trunk

    # Tree 2 (left)
    canvas.create_polygon(window_width // 4 + tree_width // 2, tree_y_offset,  # Top point of the triangle
                          window_width // 4 - tree_width, tree_y_offset + tree_height,  # Left point
                          window_width // 4 + tree_width * 2, tree_y_offset + tree_height,  # Right point
                          fill='darkgreen')  # Pine foliage

    # Tree trunk 2
    canvas.create_rectangle(window_width // 4 + tree_width, tree_y_offset + tree_height,
                             window_width // 4 + tree_width + 10, tree_y_offset + tree_height + 30, fill='brown')  # Trunk

    # Drawing house dynamically based on window size
    # House base (rectangle)
    canvas.create_rectangle(window_width - house_width - 50, window_height - house_height - house_y_offset, 
                            window_width - 50, window_height - house_y_offset, fill='lightblue')  # House body

    # House door (adjusted to be inside the house body)
    canvas.create_rectangle(window_width - house_width - 30, window_height - house_height - house_y_offset,
                             window_width - 50, window_height - house_height + 20 - house_y_offset, fill='white')  # House door

    # House window
    canvas.create_rectangle(window_width - house_width + 10, window_height - house_height - house_y_offset,
                             window_width - house_width + 40, window_height - house_height + 20 - house_y_offset, fill='white')  # House window

    # House roof (pointed roof)
    canvas.create_polygon(window_width - house_width - 50, window_height - house_height - house_y_offset, 
                          window_width - house_width // 2, window_height - house_height - house_y_offset - 50,  # Peak of the roof
                          window_width - 50, window_height - house_height - house_y_offset, fill='brown')  # Roof

# Creating the main window
root = tk.Tk()
root.title("Generative Agents Simulation")
root.geometry("800x600")  # Initial window size
root.minsize(800, 600)  # Minimum window size
is_full_screen = False  # Variable to track full-screen mode

# Bind the 'F11' key to toggle full-screen mode
root.bind("<F11>", toggle_full_screen)

# Adding a frame to center the buttons
frame = tk.Frame(root)
frame.pack(side="top", pady=60)  # Adjusted padding to move the buttons closer to the center

# Adding the Exit button in the top-left corner
exit_button = tk.Button(root, text="Exit", command=exit_application, font=('Arial', 10))
exit_button.place(x=10, y=10)

# Adding the Help button in the top-right corner
help_button = tk.Button(root, text="?", command=show_help, font=('Arial', 14), width=2, height=1)
help_button.place(x=root.winfo_width() - help_button.winfo_width() - 10, y=10)

# Adding the New Simulation button in the middle (inside frame)
new_sim_button = tk.Button(frame, text="New Simulation", command=new_simulation, font=('Arial', 14), width=20, height=2)
new_sim_button.grid(row=0, column=0, padx=10, pady=10)

# Adding the Load Simulation button in the middle (inside frame)
load_sim_button = tk.Button(frame, text="Load Simulation", command=load_simulation, font=('Arial', 14), width=20, height=2)
load_sim_button.grid(row=1, column=0, padx=10, pady=10)

# Creating a canvas for drawing
canvas = tk.Canvas(root, width=800, height=400)  # Adjusted height to leave room for buttons and the scene
canvas.pack(fill=tk.BOTH, expand=True)

# Function to draw the scene
def draw_scene():
    # Initial drawing of the scene
    update_scene()

# Call the function to draw the scene
draw_scene()

# Bind the window resize event to update the Help button position dynamically
root.bind("<Configure>", lambda event: [update_scene(event), update_help_button_position()])

# Running the main loop
root.mainloop()
