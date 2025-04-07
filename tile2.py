import os
from PIL import Image, ImageTk
from tkinter import filedialog

class Tile:
    def __init__(self, tile_type, walkable=False, interactable=False, symbol="?", image_path=None):
        self.tile_type = tile_type
        self.walkable = walkable
        self.interactable = interactable
        self.symbol = symbol
        self.image = None  
        if image_path:
            self.set_image(image_path)  

    def set_image(self, image_path):
        try:
            self.image = Image.open(image_path)  
        except IOError:
            print(f"Error: Unable to load image from {image_path}")

    def display_image(self, canvas, x, y, tile_size=32):
        if self.image:
            img = self.image.resize((tile_size, tile_size), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            canvas.create_image(x, y, image=img)
            return img  
        else:
            print(f"No image available for {self.tile_type}")
            return None

def upload_tile_image():
    file_path = filedialog.askopenfilename(title="Select Tile Image", filetypes=[("JPEG files", "*.jpg;*.jpeg")])
    if file_path:
        return file_path  
    return None  

class Grass(Tile):
    def __init__(self, symbol='+', walkable=True, image_path=None):
        image_path = image_path or upload_tile_image()  
        super().__init__("Grass", symbol=symbol, walkable=walkable, image_path=image_path)

class Water(Tile):
    def __init__(self, symbol='~', image_path=None):
        image_path = image_path or upload_tile_image()  
        super().__init__("Water", symbol=symbol, image_path=image_path)

class Soil(Tile):
    def __init__(self, symbol='#', walkable=False, image_path=None):
        image_path = image_path or upload_tile_image()  
        super().__init__("Soil", symbol=symbol, walkable=walkable, image_path=image_path)

class Bridge(Tile):
    def __init__(self, symbol='(', walkable=True, image_path=None):
        image_path = image_path or upload_tile_image()  
        super().__init__("Bridge", symbol=symbol, walkable=walkable, image_path=image_path)
