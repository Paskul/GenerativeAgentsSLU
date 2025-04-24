# llm/llm.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def generate_action_plan(sim_time, sim_vision, agent, prev_action_plan="", overseer_directives=None):
    if overseer_directives is None:
        overseer_directives = []
    """
    Generate a movement-level action plan for an agent, including a one-sentence speech.
    The output JSON must include these keys:
      - "name": string,
      - "goalxy": [int, int],
      - "direction": string (one of "up", "down", "left", "right"),
      - "speech": string (a one-sentence statement).
    """
    # Retrieve the agent's current daily plan; if none exists, use "None"
    daily_plan = getattr(agent, "daily_plan", "None")
    
    message = (
        "You are creating an action plan for an agent in a Generative Agents Simulator. "
        "The agent's decision should be a movement decision only, with no additional talking beyond a single sentence of speech. "
        "Moving up means position_y+1 relative to the current position; moving down means position_y-1; moving right means position_x+1; moving left means position_x-1. "
        "RULE: The simulation environment is a grid of size 48 by 27. Valid x coordinates are 0 to 47 and valid y coordinates are 0 to 26. "
        "The agent must not plan a move that takes it out of these bounds. "
        "RULE: The agent cannot move into or through walls. "
        "RULE: If the agent sees water and a nearby bridge, the agent must choose to use the bridge instead of moving through water. "
        "RULE: The agent should be coming up with tasks to meet the daily plan. "
        "Obey ALL rules in the message; obeying them is more important than achieving any goal. \n"
        "In addition, produce a one-sentence statement (the agent's 'speech') that expresses what the agent is thinking or saying at this moment. \n"
        "Based on the following information:\n"
        f"- Simulation time: {sim_time}\n"
        f"- Agent name: {agent.name}\n"
        f"- Agent role: {agent.role}\n"
        f"- Agent personality: {agent.personality}\n"
        f"- Agent position x: {agent.x}\n"
        f"- Agent position y: {agent.y}\n"
        f"- Agent vision: {sim_vision}\n"
        f"- Previous action plan: {prev_action_plan}\n"
        f"- Current daily plan: {daily_plan}\n"
        f"- Overseer directives (the user wants attempts to apply these to agent plans!): "
        f"{', '.join(overseer_directives) if overseer_directives else 'None'}\n\n"
        "Output an action plan strictly in JSON format with exactly these keys:\n\n"
        "  \"name\": string,\n"
        "  \"goalxy\": [int, int],\n"
        "  \"direction\": string (one of \"up\", \"down\", \"left\", \"right\"),\n"
        "  \"speech\": string (a one-sentence statement).\n"
        "Only output the JSON object."
    )
    print(message)
    try:
        completion = client.chat.completions.create(
            #model="gpt-4o-mini",
            model="o3-mini",
            messages=[{"role": "developer", "content": message}]
        )
        action_plan = completion.choices[0].message.content.strip()
        print("LLM action plan output:", action_plan)
        return action_plan
    except Exception as e:
        print(f"API call failed: {e}")
        return None


def generate_daily_action_plan(sim_date, env_summary, agent, prev_daily_plan=""):
    """
    Generate a daily action plan for an agent outlining the overall objectives for the day.
    The output JSON should include:
      - "name": the agent's name,
      - "daily_plan": a string representing the overall objectives for the day, including
                      recommended timestamps for when tasks should be attempted.
    """
    message = (
        "You are creating a daily action plan for an agent in a Generative Agents Simulator. "
        "The daily action plan should outline the overall objectives for the day—such as tasks to complete, "
        "places to visit, and people to interact with—and include recommended timestamps for when these tasks "
        "should be attempted (for example, '09:00 - Visit the farm', '14:00 - Meet the merchant at the market'). "
        "The daily plan should be conservative in the number of tasks and goals it sets for the day, "
        "to ensure the agent does not overcommit. \n"
        "The simulation environment is a grid of size 48 x 27. Valid x coordinates are 0 to 47 and valid y coordinates are 0 to 26. \n"
        "The environment is described as follows: " + env_summary + "\n"
        "RULE: The plan must not contain any moves that take the agent out of bounds. \n"
        "Based on the following information:\n"
        f"- Simulation date: {sim_date}\n"
        f"- Agent name: {agent.name}\n"
        f"- Agent role: {agent.role}\n"
        f"- Agent personality: {agent.personality}\n"
        f"- Agent position: ({agent.x}, {agent.y})\n"
        f"- Previous daily plan: {prev_daily_plan}\n\n"
        "Output a daily action plan strictly in JSON format with exactly these keys:\n"
        "  \"name\": string,\n"
        "  \"daily_plan\": string.\n"
        "Only output the JSON object."
    )
    print(message)
    try:
        completion = client.chat.completions.create(
            model="o3-mini",
            messages=[{"role": "developer", "content": message}]
        )
        daily_action_plan = completion.choices[0].message.content.strip()
        print("LLM daily action plan output:", daily_action_plan)
        return daily_action_plan
    except Exception as e:
        print(f"Daily plan API call failed: {e}")
        return None
