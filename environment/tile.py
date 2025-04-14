# environment/tile.py
import os
from PIL import Image, ImageTk
import tkinter as tk

# Compute the path to the assets folder (assumes assets folder is at project/assets)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "..", "assets")

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

    def display_image(self, canvas: tk.Canvas, x: int, y: int, tile_size=32):
        """Resize and display this tile’s image on the canvas at (x, y)."""
        if self.image:
            img = self.image.resize((tile_size, tile_size), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            canvas.create_image(x, y, image=tk_img, anchor='nw')
            # Save reference to avoid garbage collection.
            if not hasattr(canvas, 'image_refs'):
                canvas.image_refs = []
            canvas.image_refs.append(tk_img)
        else:
            # In this version, we rely solely on images.
            pass

    def __repr__(self):
        return self.symbol

# Specific tile classes with default image paths.
class Grass(Tile):
    def __init__(self, symbol='+', walkable=True):
        super().__init__(
            tile_type="Grass",
            walkable=walkable,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "grass.png")
        )

class Water(Tile):
    def __init__(self, symbol='~'):
        super().__init__(
            tile_type="Water",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "water.png")
        )

class Soil(Tile):
    def __init__(self, symbol='#', walkable=False):
        super().__init__(
            tile_type="Soil",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "soil.png")
        )

class Bridge(Tile):
    def __init__(self, symbol='(', walkable=True):
        super().__init__(
            tile_type="Bridge",
            walkable=True,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "bridge.png")
        )

class Bush(Tile):
    def __init__(self, symbol='$'):
        super().__init__(
            tile_type="Bush",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "bush.png")
        )

class Wall(Tile):
    def __init__(self, symbol='|'):
        super().__init__(
            tile_type="Wall",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "wall.png")
        )

class Path(Tile):
    def __init__(self, symbol='=', walkable=True):
        super().__init__(
            tile_type="Path",
            walkable=True,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "path.png")
        )

class Floor(Tile):
    def __init__(self, symbol='.', walkable=True):
        super().__init__(
            tile_type="Floor",
            walkable=True,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "floor.png")
        )

class Sand(Tile):
    def __init__(self, symbol=':', walkable=True):
        super().__init__(
            tile_type="Sand",
            walkable=True,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "sand.png")
        )
