# agents/agent.py

class Agent:
    def __init__(self, name, role, age, personality, x, y, vision_radius=5):
        self.name = name
        self.role = role
        self.age = age
        self.personality = personality
        self.x = x
        self.y = y
        self.vision_radius = vision_radius  # Vision range in grid units
        self.relationships = {}  # Relationships with other agents

    def get_location(self):
        return self.x, self.y

    def move(self, direction):
        # Basic movement; note: bounds checking should be handled by the simulation
        if direction == "up":
            self.y += 1 
        elif direction == "down":
            self.y -= 1
        elif direction == "left":
            self.x -= 1 
        elif direction == "right":
            self.x += 1

    def describe_agent(self):
        print(f"{self.name} - {self.role}")
        print(f"Personality: {self.personality}")
        print(f"Location: ({self.x}, {self.y})")
        print(f"Relationships: {self.relationships}")

    def get_age(self):
        return self.age

    def get_visible_entities(self, game_map, other_agents):
        """
        Scans the map and other agents within the vision radius.
        Returns a dictionary with:
          - 'tiles': a list of tuples (tile_type, (x, y)) for key tiles (non-Grass)
          - 'agents': a list of dictionaries for agents within vision (excluding self)
        """
        visible = {'tiles': [], 'agents': []}
        x0, y0 = self.x, self.y
        radius = self.vision_radius
        
        # Scan the grid for key tiles
        for y in range(max(0, y0 - radius), min(game_map.height, y0 + radius + 1)):
            for x in range(max(0, x0 - radius), min(game_map.width, x0 + radius + 1)):
                tile = game_map.grid[y][x]
                if tile.tile_type != "Grass":  # Define key tile as any non-Grass tile
                    visible['tiles'].append((tile.tile_type, (x, y)))
        
        # Find nearby agents (excluding self)
        for agent in other_agents:
            if agent.name == self.name:
                continue
            ax, ay = agent.get_location()
            if abs(ax - x0) <= radius and abs(ay - y0) <= radius:
                visible['agents'].append({'name': agent.name, 'location': (ax, ay)})
                
        return visible
