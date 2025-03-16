from address import Address
# Notes for further development
    # agents or map store neighbors?
    # edges have null object design pattern
class Tile:  
    def __init__(self, tile_type, walkable = False, interactable = False, symbol = "?", address = None):
        self.tile_type = tile_type
        self.walkable = walkable
        self.interactable = interactable
        self.symbol = symbol
        self.address = address

    def set_address(self, x, y):
        self.address = Address(x,y)
        return self
    
    def __repr__(self):
        return self.symbol

# Types of Tiles
class Grass(Tile):
    def __init__(self, symbol='+', walkable = True):
        super().__init__("Grass", symbol=symbol, walkable=walkable)

class Water(Tile):
    def __init__(self, symbol = '~'):
        super().__init__("Water", symbol=symbol)

class Soil(Tile):
    def __init__(self, symbol = '#', walkable = False):
        super().__init__("Soil", symbol=symbol, walkable=walkable)

# Details
class Bridge(Tile):
    def __init__(self, symbol='(', walkable=True):
        super().__init__("Bridge", symbol=symbol, walkable=walkable)

class Bush(Tile):
    def __init__(self, symbol = '$'):
        super().__init__("Bush", symbol=symbol)

class Wall(Tile):
    def __init__(self, symbol = '|'):
        super().__init__("Wall", symbol=symbol)

class Path(Tile):
    def __init__(self, symbol = '=',walkable=True):
        super().__init__("Path", symbol=symbol, walkable=walkable)

class Floor(Tile):
    def __init__(self, symbol = '.',walkable=True):
        super().__init__("Floor", symbol=symbol, walkable=walkable)

class Sand(Tile):
    def __init__(self, symbol = ':',walkable=True):
        super().__init__("Sand", symbol=symbol, walkable=walkable)