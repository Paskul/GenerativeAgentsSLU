# environment/map.py

from .tile import Grass, Water, Soil, Bridge, Bush, Wall, Path, Floor, Sand

class Map:
    def __init__(self, width=48, height=27):
        self.width = width
        self.height = height
        # Create a grid filled with Grass by default
        self.grid = [[Grass() for _ in range(width)] for _ in range(height)]
        self.create_base_map()

    def set_tile(self, x, y, tile_cls):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = tile_cls()

    def fill_tiles(self, x_topleft, y_topleft, width, height, tile_cls):
        for y in range(height):
            for x in range(width):
                if 0 <= x_topleft + x < self.width and 0 <= y_topleft + y < self.height:
                    self.grid[y_topleft + y][x_topleft + x] = tile_cls()

    def create_base_map(self):
        # Grass base layer
        self.fill_tiles(0, 0, self.width, self.height, Grass)
        # River (Water)
        self.fill_tiles(0, 11, self.width, 3, Water)
        # Farm patches (Soil)
        self.fill_tiles(1, 15, 5, 5, Soil)
        self.fill_tiles(1, 21, 5, 5, Soil)
        self.fill_tiles(7, 21, 5, 5, Soil)
        self.fill_tiles(13, 21, 5, 5, Soil)
        self.fill_tiles(19, 21, 5, 5, Soil)
        # Bridges
        self.fill_tiles(8, 11, 3, 3, Bridge)
        self.fill_tiles(37, 11, 3, 3, Bridge)
        # Apartments (Walls and Floors)
        self.fill_tiles(0, 0, 21, 5, Wall)
        self.fill_tiles(0, 5, 5, 5, Wall)
        self.fill_tiles(1, 1, 4, 3, Floor)
        self.fill_tiles(7, 1, 3, 3, Floor)
        self.fill_tiles(12, 1, 3, 3, Floor)
        self.fill_tiles(17, 1, 3, 3, Floor)
        self.fill_tiles(1, 6, 3, 3, Floor)
        # Store (Walls and Floors)
        self.fill_tiles(33, 1, 14, 9, Wall)
        self.fill_tiles(34, 2, 12, 7, Floor)
        # Paths
        self.fill_tiles(4, 5, 2, 2, Path)
        self.fill_tiles(6, 6, 9, 4, Path)
        self.fill_tiles(9, 4, 1, 2, Path)
        self.fill_tiles(14, 4, 1, 2, Path)
        self.set_tile(4, 4, Path)
        self.fill_tiles(15, 6, 19, 1, Path)
        self.fill_tiles(8, 10, 3, 1, Path)
        self.fill_tiles(37, 9, 3, 2, Path)
        # Bushes
        self.set_tile(5, 7, Bush)
        self.set_tile(6, 5, Bush)
        self.set_tile(8, 5, Bush)
        self.set_tile(10, 5, Bush)
        self.set_tile(13, 5, Bush)
        self.set_tile(15, 5, Bush)
        self.set_tile(18, 5, Bush)
        self.set_tile(20, 5, Bush)
        # Beach (Sand)
        self.fill_tiles(14, 14, 19, 1, Sand)
        self.fill_tiles(15, 15, 17, 1, Sand)
        self.fill_tiles(16, 16, 15, 1, Sand)

    def display(self):
        for row in self.grid:
            print(''.join(tile.symbol for tile in row))

    def render_map(self, canvas, tile_size=32):
        """
        Renders the map's tiles onto the given Tkinter canvas.
        Each tile is drawn at (x * tile_size, y * tile_size).
        """
        # Initialize a list to store references to tile images
        if not hasattr(canvas, 'image_refs'):
            canvas.image_refs = []

        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                screen_x = x * tile_size
                screen_y = y * tile_size
                tile.display_image(canvas, screen_x, screen_y, tile_size)

