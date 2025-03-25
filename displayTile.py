import tkinter as tk
from tile import Grass, Water, Soil, Bridge  # Import your tile classes

# Initialize Tkinter window
root = tk.Tk()
root.title("Tile Image Upload Example")
root.geometry("800x600")

# Create a canvas to draw the map (tile grid)
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill=tk.BOTH, expand=True)

# Define the size of each tile
tile_size = 64

# Create some tile objects with JPEG images
grass_tile = Grass(image_path=None)  # Will trigger image upload dialog
water_tile = Water(image_path=None)  # Will trigger image upload dialog
soil_tile = Soil(image_path=None)   # Will trigger image upload dialog
bridge_tile = Bridge(image_path=None)  # Will trigger image upload dialog

# Sample tile coordinates on the map (grid)
tiles = [
    (grass_tile, 100, 100),  # Grass tile at position (100, 100)
    (water_tile, 200, 100),  # Water tile at position (200, 100)
    (soil_tile, 300, 100),   # Soil tile at position (300, 100)
    (bridge_tile, 400, 100),  # Bridge tile at position (400, 100)
]

# Draw the tiles on the canvas
for tile, x, y in tiles:
    tile.display_image(canvas, x, y, tile_size)

# Start the Tkinter main loop
root.mainloop()
