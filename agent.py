"""this class defines the agent class and is focused on defining the inividual agent"""

from address import Address

class Agent:
    def __init__(self,name,role,age,personality,x,y):
        self.name = name
        self.role = role
        self.age = age
        self.personality = personality
        self.x = x
        self.y = y  
        self.relationships = {} #dictionary to hold the agents relationships with one another 

    def get_location(self):
        return self.x, self.y
    
    def move_agent(self, agent, direction):
        new_x, new_y = agent.x, agent.y

        if direction == "up":
            new_y -= 1
        elif direction == "down":
            new_y += 1
        elif direction == "left":
            new_x -= 1
        elif direction == "right":
            new_x += 1
        else:#not a real direction -- invalid 
            return

        if 0 <= new_x < self.map.width and 0 <= new_y < self.map.height:#check if within bounds 
            tile = self.map.grid[new_y][new_x]
            if tile.walkable:#agent cant walk into a tree or a bush etc. 
                agent.x = new_x
                agent.y = new_y
        
    def describe_agent(self):#likely can attatch this to button if user wants to click on agent to learn more about them or beneath map have some UI so we can see agent info 
         print(f"{self.name} - {self.role}")
         print(f"Personality: {self.personality}")
         print(f"Location: ({self.x}, {self.y})")
         print(f"Relationships: {self.relationships}")

    def get_age(self):
        return self.age
    

    #gets list of what the tiles are around agent can pass this list to llm to determine what next action is 
    def get_surroundings(self, agent, radius=5):
        visible_tiles = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x, y = agent.x + dx, agent.y + dy
                if 0 <= x < self.map.width and 0 <= y < self.map.height:
                    tile = self.map.grid[y][x]
                    visible_tiles.append(Address(x, y, tile.tile_type))
        return visible_tiles



