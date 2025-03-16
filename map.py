from tile import *
class Map:
    def __init__(self, width=48,height=27):
        self.width = width
        self.height = height
        self.grid = [[Grass() for _ in range(width)] for _ in range(height)] # empty map filled w spaces as placeholders
        self.create_base_map()
        self.display()

    # Potential need to add error handling if attempting to place tile out of bounds
    """Set a specific type of tile at coordinates (x, y)"""
    def set_tile(self, x, y, tile_type): 
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = tile_type() # y-th row and x-th column in row

    """Fill a rectangular area with a terrain type tile"""
    def fill_tiles(self, x_topleft, y_topleft, width, depth, tile_type):
        for x in range(width):
            for y in range(depth):
                if 0 <= x_topleft + x < self.width and 0 <= y_topleft + y < self.height:
                    self.grid[y_topleft + y][x_topleft + x] = tile_type()

    def create_base_map(self):
        """Adds grass, river, and farmland"""
        self.fill_tiles(0, 0, self.width, self.height, Grass) # grass base layer
        self.fill_tiles(0, 11, self.width, 3, Water) # middle river
        self.fill_tiles(1, 15, 5, 5, Soil) # farm patch 1
        self.fill_tiles(1, 21, 5, 5, Soil) # farm patch 2
        self.fill_tiles(7, 21, 5, 5, Soil) # farm patch 3
        self.fill_tiles(13, 21, 5, 5, Soil) # farm patch 4
        self.fill_tiles(19, 21, 5, 5, Soil) # farm patch 5
        
        """Creates bridges"""
        self.fill_tiles(8,11,3,3,Bridge) # bridge 1
        self.fill_tiles(37,11,3,3,Bridge) # bridge 2

        """Creates apartments"""
        self.fill_tiles(0,0,21,5,Wall) # apartments 1-4
        self.fill_tiles(0,5,5,5,Wall) # apartment 5
        self.fill_tiles(1,1,4,3,Floor) # apartment 1 flooring
        self.fill_tiles(7,1,3,3,Floor) # apartment 2 flooring
        self.fill_tiles(12,1,3,3,Floor) # apartment 3 flooring
        self.fill_tiles(17,1,3,3,Floor) # apartment 4 flooring
        self.fill_tiles(1,6,3,3,Floor) # apartment 5 flooring

        """Builds store"""
        self.fill_tiles(33,1,14,9,Wall) # wall of store
        self.fill_tiles(34,2,12,7,Floor) # floor of store

        """Builds paths"""
        self.fill_tiles(4,5,2,2,Path) # path outside apartments 1 and 5
        self.fill_tiles(6,6,9,4,Path) # path area outside apartments
        self.fill_tiles(9,4,1,2,Path) # path apt 2
        self.fill_tiles(14,4,1,2,Path) # path apt 3
        self.fill_tiles(19,4,1,2,Path) # path apt 4
        self.set_tile(4,4,Path) # path apartment 1
        self.fill_tiles(15,6,19,1,Path) # path to store
        self.fill_tiles(8,10,3,1,Path) # path to bridge north
        self.fill_tiles(37,9,3,2,Path) # path from store to bridge

        """Sets bushes"""
        self.set_tile(5,7,Bush)
        self.set_tile(6,5,Bush)
        self.set_tile(8,5,Bush)
        self.set_tile(10,5,Bush)
        self.set_tile(13,5,Bush)
        self.set_tile(15,5,Bush)
        self.set_tile(18,5,Bush)
        self.set_tile(20,5,Bush)

        """Builds beach"""
        self.fill_tiles(14,14,19,1,Sand)
        self.fill_tiles(15,15,17,1,Sand)
        self.fill_tiles(16,16,15,1,Sand)
        

    def display(self):
        for row in self.grid:
            print(''.join(tile.symbol for tile in row))

Map()
