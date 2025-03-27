from agent import Agent

"""This class stores all agent functionality & handles their movements and surroundings"""

class ManageAgents:
    def __init__ (self,map):
        self.map = map
        #want to add in the relationships thing clara and otto are married bc they are both shop keepers 
        #where they start in the game will change once map is more established: just doing 0,0 for now. 
        #we will need to go in and have the llm fill in some of these attributes, not sure if I should leave them blank at this point 
        self.all_agents = [
            Agent("Ada","Farmer",29,"Smart",0,0),
            Agent("Gus","Fisherman",32,"Shy",0,0),
            Agent("Clara","Shop Owner",40,"Friendly",0,0),
            Agent("Otto","Shop Owner",4,"Persuasive",0,0),
            Agent("Alan","Farmer",57,"Grumpy",0,0),
            Agent("Olive","Artisan",30,"Creative",0,0),
            Agent("Mavis","Farmer",25,"Bubbly",0,0),
            Agent("Finn","Student",9,"Hyper",0,0)
        ]


