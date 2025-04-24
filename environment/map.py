# environment/map.py

from .tile import Grass, Water, Soil, Bridge, Bush, Wall, Path, Floor, Sand, BedTop, BedBottom, BenchTop, BenchBottom

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
        # Beds
        self.set_tile(1,6,BedTop) # Bed #5
        self.set_tile(1,7,BedBottom)
        self.set_tile(1,1,BedTop) # Bed #1
        self.set_tile(1,2,BedBottom)
        self.set_tile(7,1,BedTop) # Bed #2
        self.set_tile(7,2,BedBottom)
        self.set_tile(12,1,BedTop) # Bed #3
        self.set_tile(12,2,BedBottom)
        self.set_tile(17,1,BedTop) # Bed #4
        self.set_tile(17,2,BedBottom)

    def get_layout_summary(self):
        """
        Provides a detailed overview of this 48x27 map, specifying
        major features and their coordinates.
        
        Coordinate System:
        - x ranges from 0 (left) to 47 (right)
        - y ranges from 0 (top) to 26 (bottom)
        - (x=0, y=0) is top-left corner

        Features:
        - River (Water): spans rows y=11..13 (full width x=0..47).
        - Bridges:
            1) x=8..10, y=11..13
            2) x=37..39, y=11..13
        - Apartments (top-left):
            - Large walled area from x=0..20, y=0..4
            - Another walled block from x=0..4, y=5..9
            - Floors at x=1..4,7..9,12..14,17..19 (y=1..3) and x=1..3 (y=6..8)
        - Store (top-right):
            - Walls from x=33..46, y=1..9
            - Floors from x=34..45, y=2..8
        - Farm Patches (Soil) near bottom:
            - (x=1..5, y=15..19), (x=1..5, y=21..25),
                (x=7..11, y=21..25), (x=13..17, y=21..25), (x=19..23, y=21..25)
        - Beach (Sand) around x=14..32, y=14..16 (middle-bottom).
        - Bushes scattered near (x=6..20, y=5..7), e.g., x=5,6,8,10,13,15,18,20 (y=5 or y=7).
        - Paths connect apartments, store, and farmland.
        - Grass is the base tile everywhere else.
        """
        return (
            "This map is 48 tiles wide (x=0..47) and 27 tiles tall (y=0..26). "
            "Rows y=11..13 contain a river that spans the entire width. Bridges cross the river at x=8..10 and x=37..39, y=11..13. "
            "Apartments occupy the top-left, with walls in x=0..20, y=0..4 and x=0..4, y=5..9, plus floors at x=1..4,7..9,12..14,17..19 (y=1..3), etc. "
            "A store is at x=33..46, y=1..9, with floors at x=34..45, y=2..8. "
            "Farm patches (Soil) appear near the bottom, e.g. x=1..5,y=15..19 and x=1..5,y=21..25, among others. A sand beach lies around x=14..32, y=14..16. "
            "Bushes are placed near x=6..20,y=5..7, and multiple paths connect these areas. "
            "Grass is the default tile, water forms the river, soil for farmland, sand for the beach, walls/floors for buildings, and bushes/paths/bridges in fixed positions."
        )

    def display(self):
        for row in self.grid:
            print(''.join(tile.symbol for tile in row))

    def is_walkable(self, x: int, y: int) -> bool:
        """True if (x, y) is on-map **and** its tile is walkable."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x].walkable
        return False

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

