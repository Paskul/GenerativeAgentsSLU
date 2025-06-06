class Agent:
    def __init__(self, name, role, age, personality, x, y, vision_radius=5):
        self.name = name
        self.role = role
        self.age = age
        self.personality = personality
        self.x = x
        self.y = y
        self.vision_radius = vision_radius  # Vision range in grid units
        self.relationships = {}  # A dictionary to hold relationship scores with other agents.
        self.daily_plan = ""      # To store the agent's overall daily plan.
        self.daily_plan_date = None  # Date of the current daily plan.
        self.speech = ""          # The last generated one-sentence speech.

    def get_location(self):
        return self.x, self.y

    def move(self, direction):
        # Basic movement with no bounds checking (bounds are managed by the simulation manager).
        if direction == "up":
            self.y += 1 
        elif direction == "down":
            self.y -= 1
        elif direction == "left":
            self.x -= 1 
        elif direction == "right":
            self.x += 1

    def update_relationship(self, other_agent, delta):
        # Update the relationship status between agents
        # positive delta indicates an increased relationship
        # clamped between -100 and 100 (more is better)
        # WARNING - NOT USED WELL IN FINAL PRODUCT
        current = self.relationships.get(other_agent.name, 0)
        new_value = current + delta
        # Clamp
        new_value = max(-100, min(new_value, 100))
        self.relationships[other_agent.name] = new_value
        print(f"{self.name}'s relationship with {other_agent.name} updated to {new_value}")

    def get_visible_entities(self, game_map, other_agents):
        # scan the surrounding area in vision_radius
        # looks for tiles and other agents
        # based on agents current position as center
        visible = {'tiles': [], 'agents': []}
        x0, y0 = self.x, self.y
        radius = self.vision_radius
        
        # Scan the grid for key (non-Grass) tiles.
        for y in range(max(0, y0 - radius), min(game_map.height, y0 + radius + 1)):
            for x in range(max(0, x0 - radius), min(game_map.width, x0 + radius + 1)):
                tile = game_map.grid[y][x]
                if tile.tile_type != "Grass":  # Only add non-grass tiles.
                    visible['tiles'].append((tile.tile_type, (x, y)))
        
        # Include nearby agents (other than self), along with their speech.
        for agent in other_agents:
            if agent is self:
                continue
            ax, ay = agent.get_location()
            if abs(ax - x0) <= radius and abs(ay - y0) <= radius:
                agent_info = {
                    "name": agent.name,
                    "position": (ax, ay),
                    "speech": agent.speech  # May be an empty string if no speech.
                }
                visible['agents'].append(agent_info)
                
        return visible

    def describe_agent(self):
        print(f"{self.name} - {self.role}")
        print(f"Personality: {self.personality}")
        print(f"Location: ({self.x}, {self.y})")
        print(f"Relationships: {self.relationships}")
