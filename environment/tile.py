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
        # assign image to tile in render
        try:
            self.image = Image.open(image_path)
        except IOError:
            print(f"Error: Unable to load image from {image_path}")

    def display_image(self, canvas: tk.Canvas, x: int, y: int, tile_size=32):
        # render image through resize and display on canvas at image (x,y)
        if self.image:
            img = self.image.resize((tile_size, tile_size), Image.ANTIALIAS)
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
    def __init__(self, symbol='#', walkable=True):
        super().__init__(
            tile_type="Soil",
            walkable=True,
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

class BedTop(Tile):
    def __init__(self, symbol = '0'):
        super().__init__(
            tile_type="BedTop",
            walkable=True,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "bedtop.png")
        )

class BedBottom(Tile):
    def __init__(self, symbol = '0'):
        super().__init__(
            tile_type="BedBottom",
            walkable=True,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "bedbottom.png")
        )

class BenchTop(Tile):
    def __init__(self, symbol = '%'):
        super().__init__(
            tile_type="BenchTop", 
            walkable=True,
            symbol=symbol, 
            image_path=os.path.join(ASSETS_DIR, "benchtop.png")
        )

class BenchBottom(Tile):
    def __init__(self, symbol = '0'):
        super().__init__(
            tile_type="BenchBottom", 
            walkable=True,
            symbol=symbol, 
            image_path=os.path.join(ASSETS_DIR, "benchbottom.png")
        )

class CounterBottom(Tile):
    def __init__(self,symbol = '|'):
        super().__init__(
            tile_type="CounterBottom",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "counterbottom.png")
        )

class CounterMiddle(Tile):
    def __init__(self,symbol = '|'):
        super().__init__(
            tile_type="CounterMiddle",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "countermiddle.png")
        )

class CounterTop(Tile):
    def __init__(self,symbol = '|'):
        super().__init__(
            tile_type="CounterTop",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "countertop.png")
        )

class BinApple(Tile):
    def __init__(self,symbol = '@'):
        super().__init__(
            tile_type="BinApple",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "binapple.png")
        )
        
class BinCucumber(Tile):
    def __init__(self,symbol = '@'):
        super().__init__(
            tile_type="BinCucumber",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "bincucumber.png")
        )

class BinEggplant(Tile):
    def __init__(self,symbol = '@'):
        super().__init__(
            tile_type="BinEggplant",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "bineggplant.png")
        )

class BinPotato(Tile):
    def __init__(self,symbol = '@'):
        super().__init__(
            tile_type="BinPotato",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "binpotato.png")
        )

class TreeOak(Tile):
    def __init__(self,symbol = '5'):
        super().__init__(
            tile_type="TreeOak",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "treeoak.png")
        )

class TreePine(Tile):
    def __init__(self,symbol = '5'):
        super().__init__(
            tile_type="TreePine",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "treepine.png")
        )

class TreeOrange(Tile):
    def __init__(self,symbol = '5'):
        super().__init__(
            tile_type="TreeOrange",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "treeorange.png")
        )

class TreePink(Tile):
    def __init__(self,symbol = '5'):
        super().__init__(
            tile_type="TreePink",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "treepink.png")
        )

class TreePurple(Tile):
    def __init__(self,symbol = '5'):
        super().__init__(
            tile_type="TreePurple",
            walkable=False,
            symbol=symbol,
            image_path=os.path.join(ASSETS_DIR, "treepurple.png")
        )
