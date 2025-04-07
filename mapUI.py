import tkinter as tk
from PIL import Image,ImageTk # from pillow install imaging objects
from map import Map  # Import the Map class
from tile import Tile  # Import the Tile class
import os

class MapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Map GUI")

        # Hardcoded dimensions for the window
        self.window_width = 1920  # Adjust as needed (48 tiles * 20 px each)
        self.window_height = 1080  # Adjust as needed (27 tiles * 20 px each)

        # Get screen dimensions to calculate the position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate x and y coordinates for the window to be centered
        x_coord = (screen_width // 2) - (self.window_width // 2)
        y_coord = (screen_height // 2) - (self.window_height // 2)

        # Set the geometry of the window (width x height + x_offset + y_offset)
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x_coord}+{y_coord}")

        # Define the number of tiles in each dimension
        self.tiles_x = 48
        self.tiles_y = 27

        # Calculate tile dimensions to fit the hardcoded window size
        self.tile_width = self.window_width / self.tiles_x
        self.tile_height = self.window_height / self.tiles_y

        # Create a canvas that spans the entire window
        self.canvas = tk.Canvas(self.root, width=self.window_width, height=self.window_height, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Initialize the map
        self.map = Map(width=self.tiles_x, height=self.tiles_y)

        # Render the map
        self.render_map()

    def load_tile_images(self):
        tile_images = {}
        tile_types = ["bedbottom", "bedtop", "benchbottom", "benchtop","bridge","bush","floor","grass","path","sand","soil","wall","water"]

        for tile_type in tile_types:
            #check that the image is in the tiles directory
            image_path = os.path.join("tiles",f"{tile_type.lower()}.png")
            try:
                # open and resize image to 20x20 pixels
                image = Image.open(image_path)
                image = image.resize((int(self.tile_width), int(self.tile_height)), Image.Resampling.LANCZOS)
                # convert image to PhotoImage format for Tkinter
                tile_images[tile_type] = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                print(f"Error: {image_path} not found.")
        return tile_images

    def render_map(self):
        """Render the map onto the canvas."""
        self.tile_images = self.load_tile_images()
        
        for y, row in enumerate(self.map.grid):
            for x, tile in enumerate(row):
                # Calculate coordinates for each rectangle
                x1 = x * self.tile_width
                y1 = y * self.tile_height

                tile_image = self.tile_images.get(tile.tile_type.lower())
                if tile_image:
                    self.canvas.create_image(x1,y1, anchor = tk.NW, image = tile_image)
                else:
                    color = self.get_tile_color(tile)
                    self.canvas.create_rectangle(x1, y1, x1+self.tile_width, y1+self.tile_height, fill=color, outline="black")

    def get_tile_color(self, tile):
        """Return a color based on the tile type."""
        color_mapping = {
            "Grass": "green",
            "Water": "blue",
            "Soil": "brown",
            "Bridge": "tan",
            "Bush": "darkgreen",
            "Wall": "gray",
            "Path": "lightgray",
            "Floor": "beige",
            "Sand": "yellow"
        }
        return color_mapping.get(tile.tile_type, "white")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MapGUI(root)
    root.mainloop()










"""
root = tk.Tk()

# width= root.winfo_screenwidth()               
# height= root.winfo_screenheight() 
# root.geometry("%dx%d" % (width, height)) # sets window size, can also do like ("800x500")

root.geometry("800x500")

root.title("Generative Agents Map")

label = tk.Label(root, text="Hello World!", font=('Arial', 18))
label.pack(padx=20, pady=20)

textbox = tk.Text(root, height=3, font=('Arial', 16))
textbox.pack(padx=10,pady=10)

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1) # stretechs buttons to fill
buttonframe.columnconfigure(1, weight=1) # stretechs buttons to fill
buttonframe.columnconfigure(2, weight=1) # stretechs buttons to fill

btn1 = tk.Button(buttonframe,text="1", font=('Arial', 18))
btn1.grid(row=0, column=0, sticky=tk.W+tk.E)

btn2 = tk.Button(buttonframe,text="2", font=('Arial', 18))
btn2.grid(row=0, column=1, sticky=tk.W+tk.E)

btn3 = tk.Button(buttonframe,text="3", font=('Arial', 18))
btn3.grid(row=0, column=2, sticky=tk.W+tk.E)

btn4 = tk.Button(buttonframe,text="4", font=('Arial', 18))
btn4.grid(row=1, column=0, sticky=tk.W+tk.E)

btn5 = tk.Button(buttonframe,text="5", font=('Arial', 18))
btn5.grid(row=1, column=1, sticky=tk.W+tk.E)

btn6 = tk.Button(buttonframe,text="6", font=('Arial', 18))
btn6.grid(row=1, column=2, sticky=tk.W+tk.E)

buttonframe.pack(fill='x')

anotherbtn = tk.Button(root, text="TEST")
anotherbtn.place(x=200,y=200, height=100, width=100)

root.mainloop()
"""
