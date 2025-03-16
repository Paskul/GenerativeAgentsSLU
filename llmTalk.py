import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

# -------- TO-DO START --------
# need to import sim time from (active) simulator class
# need to import agent info from agent class
# need to add information of other agents 'daily plan'
# add a input validation feature
'''
try:
    simTime = float(input("Simulation time?: "))
    agentX = float(input("Current X coordinate?: "))
    agentY = float(input("Current Y coordinate?: "))
except ValueError:
    print("Error: Coordinates and time must be numeric.")
    exit()
'''
# add a log and debug feature
'''
import json

response = completion.choices[0].message.content
print(response)

# Log the response
with open("agent_action_plans.log", "a") as log_file:
    log_file.write(response + "\n")
'''
# -------- TO-DO END --------

try:
    simTime = input("What time is it in the simulation?: ")
    simVision = input("What does the agent see?: ")

    agentName = input("Which agent is this?: ")
    agentRole = input("What is their role?: ")
    agentPersonality = input("What is their personality?: ")
    agentX = input("What is their current X coordinate?: ")
    agentY = input("What is their current Y coordinate?: ")
    agentPrevActionPlan = input("What was their previous action plan?: ")

    message = (
        "You are creating action plans for Agents in a Generative Agents Simulator, similar to the paper, "
        "'Generative Agents: Interactive Simulacra of Human Behavior' by Stanford University. "
        "Based on this current information:\n"
        f"- Simulation time: {simTime}\n"
        f"- Agent name: {agentName}\n"
        f"- Agent role: {agentRole}\n"
        f"- Agent personality: {agentPersonality}\n"
        f"- Agent position (x,y): ({agentX}, {agentY})\n"
        f"- Agent vision: {simVision}\n"
        f"- Previous action plan: {agentPrevActionPlan}\n\n"
        "Create and ONLY output an action plan strictly following this JSON format:\n"
        "{\n"
        '  "name": "<agent name>",\n'
        '  "role": "<agent role>",\n'
        '  "personality": "<agent personality>",\n'
        '  "goalxy": [<goal_x>, <goal_y>],\n'
        '  "goaltask": "<goal task for agent>"\n'
        "}\n\n"
        "You may adjust agent roles and personalities over time based on prior actions or conditions."
    )
except Exception as e:
    print(f"Forming message with Agent/Sim varriables failed: {e}")
    exit()

try:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "developer",
            "content": message
        }]
    )
    print(completion.choices[0].message.content)

except Exception as e:
    print(f"API call failed: {e}")
    exit()