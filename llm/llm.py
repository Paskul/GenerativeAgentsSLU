# llm/llm.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def generate_action_plan(sim_time, sim_vision, agent, prev_action_plan=""):
    """
    Generate an action plan for an agent given the current simulation time,
    agent's vision, and agent details.
    The output JSON should include:
      - "name": the agent's name,
      - "goalxy": [target_x, target_y],
      - "direction": string (one of "up", "down", "left", or "right").
    """
    message = (
        "You are creating an action plan for an agent in a Generative Agents Simulator. "
        "The agent's decision should be a movement decision only, with no additional talking. "
        "IMPORTANT: The agent cannot move into or through walls. "
        "If the agent sees water and a nearby bridge, the agent must choose to use the bridge instead of moving through the water. "
        "Based on the following information:\n"
        f"- Simulation time: {sim_time}\n"
        f"- Agent name: {agent.name}\n"
        f"- Agent role: {agent.role}\n"
        f"- Agent personality: {agent.personality}\n"
        f"- Agent position: ({agent.x}, {agent.y})\n"
        f"- Agent vision: {sim_vision}\n"
        f"- Previous action plan: {prev_action_plan}\n\n"
        "Output an action plan strictly in JSON format with exactly these keys:\n"
        "  \"name\": string,\n"
        "  \"goalxy\": [int, int],\n"
        "  \"direction\": string (one of \"up\", \"down\", \"left\", \"right\").\n"
        "Only output the JSON object."
    )
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "developer", "content": message}]
        )
        action_plan = completion.choices[0].message.content.strip()
        print("LLM action plan output:", action_plan)
        return action_plan
    except Exception as e:
        print(f"API call failed: {e}")
        return None
