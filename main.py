from agentC import Agent

#TESTING: agent class backbone 

#example agent, i think to keep things in line we can probably have a set of 10 or 
#so personality traits and each character has a bool for them, it will be hard to keep track
#if every agent has 5 different traits etc. 

#also to implement later once map is much more established where agent home is, we can hard code this to be the agents start 
elijah = Agent("Elijah","Shop Owner",40,{"Friendly": False,"Cheap":True},0,0)
nancy = Agent("Nancy","Student",7,{"Freindly":True,"Cheap":False},0,0)

print("Nancy is",nancy.get_age(),"years old")

nancy.describe_agent()

nancy.move("up")# should be (0,1)
nancy.move("right")# should be (1,1) after the call
nancy.move("right")#should be (2,1) after the call 

nancy.describe_agent()
