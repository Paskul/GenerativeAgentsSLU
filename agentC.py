class Agent:
    def __init__(self,name,role,age,personality,x,y):
        self.name = name
        self.role = role
        self.age = age
        self.personality = personality
        self.x = x
        self.y = y
        #self.vision_radius = ?? what should vision be for each agent 5 tiles, need to decide this later
        self.relationships = {} #dictionary to hold the agents relationships with one another 

    def get_location(self):
        return self.x, self.y
    
    def move(self,direction):#will most likely need to be changed based on how we are storing the change in direction, just a basic function for now
        #will also need to add bounds checking when the map is implemented more
        if direction == "up":
            self.y += 1 
        elif direction == "down":
            self.y -= 1
        elif direction == "left":
            self.x -= 1 
        elif direction == "right":
            self.x += 1
        
        
    def describe_agent(self):#likely can attatch this to button if user wants to click on agent to learn more about them or beneath map have some UI so we can see agent info 
         print(f"{self.name} - {self.role}")
         print(f"Personality: {self.personality}")
         print(f"Location: ({self.x}, {self.y})")
         print(f"Relationships: {self.relationships}")

    def get_age(self):
        return self.age
    

    #would create agent be useful where it creates the first five in the general states etc/ 


