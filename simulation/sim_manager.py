import time, json
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import tkinter.font as tkFont
from GenerativeAgents.agents.agent       import Agent
from GenerativeAgents.environment.map    import Map
from GenerativeAgents.simulation.time_manager import TimeManager
from GenerativeAgents.llm.llm            import (
    generate_action_plan,
    generate_daily_action_plan,
)

class SimulationManager:
    def __init__(self, agents, environment, start_time=None,
                 time_step=timedelta(minutes=10)):
        self.agents       = agents
        self.environment  = environment
        self.time_manager = TimeManager(start_time=start_time,
                                        time_step=time_step)
        self.active       = True
        self.step_count   = 0

        # --- UI shared logs & directives --------------------------------------
        self.message_log: list[str]  = ["Waiting for agents to generate action plans…"]
        self.overseer_directives: list[dict] = []       
        self.daily_ready = False

        # initialise relationships to 0
        for a in agents:
            for b in agents:
                if a is not b:
                    a.relationships.setdefault(b.name, 0)

    # ---------------------------------------------------------------- overseer
    def add_directive(self, text: str) -> None:
        """Store a directive from the player and log it."""
        self.overseer_directives.append({"text": text, "ttl": 2})
        self.add_message(text, "Overseer")

    # ---------------------------------------------------------------- utilities
    def add_message(self, text: str, speaker: Optional[str] = None) -> None:
        line = f"{speaker}: {text}" if speaker else text
        self.message_log.append(line)
        if len(self.message_log) > 20:
            self.message_log.pop(0)

    @staticmethod
    def clean_llm_output(text: str) -> str:
        text = text.strip()
        if text.startswith("```") and text.endswith("```"):
            text = text.strip("`")
            if text.lower().startswith("json"):
                text = text[4:].strip()
        return text

    # ---------------------------------------------------------------- daily planning
    def update_daily_plans(self, now):
        """Generate daily plans (one per agent) concurrently; no overseer input."""
        self.daily_ready = False

        env_summary = (self.environment.get_layout_summary()
                       if hasattr(self.environment, "get_layout_summary")
                       else f"{self.environment.width}×{self.environment.height} grid")

        pending = [a for a in self.agents
                   if getattr(a, "daily_plan_date", None) != now.date()]

        if not pending:            # everyone already has today’s plan
            self.daily_ready = True
            return

        date_str = now.strftime("%Y-%m-%d")

        # run LLM calls in parallel
        with ThreadPoolExecutor(max_workers=len(pending)) as tp:
            fut_map = {
                tp.submit(
                    generate_daily_action_plan,
                    date_str,
                    env_summary,
                    ag,
                    getattr(ag, "daily_plan", "")     # prev_daily_plan
                    # (no overseer_directives arg)
                ): ag for ag in pending
            }
            for fut in fut_map:
                ag = fut_map[fut]
                try:
                    raw = fut.result()
                    if not raw:
                        continue
                    plan = json.loads(self.clean_llm_output(raw))
                    ag.daily_plan      = plan.get("daily_plan", "")
                    ag.daily_plan_date = now.date()
                    self.add_message("New daily plan set.", ag.name)
                except Exception as e:
                    print(f"Daily-plan JSON error for {ag.name}:", e)

        self.daily_ready = True

    # ---------------------------------------------------------------- micro planning
    def update_agent(self, ag, now, directives):
        vision    = ag.get_visible_entities(self.environment, self.agents)
        prev_plan = getattr(ag, "prev_action_plan", "")
        raw = generate_action_plan(
            now.strftime("%H:%M"), vision, ag, prev_plan,
            directives                        # ← pass only micro-step directives
        )
        if not raw:
            return

        try:
            plan = json.loads(self.clean_llm_output(raw))
            direction = plan.get("direction")
            speech    = plan.get("speech", "").strip()
        except Exception as e:
            print("Step JSON error:", e); return

        # candidate coordinates
        nx, ny = ag.x, ag.y
        if   direction == "up"   : ny += 1
        elif direction == "down" : ny -= 1
        elif direction == "left" : nx -= 1
        elif direction == "right": nx += 1

        # bounds & walkability check
        legal_move = False
        if 0 <= nx < self.environment.width and 0 <= ny < self.environment.height:
            tgt_tile = self.environment.grid[ny][nx]
            legal_move = getattr(tgt_tile, "walkable", False)

        if legal_move:
            ag.move(direction)
            ag.prev_action_plan = raw
            ag.speech           = speech
            if speech:
                self.add_message(speech, ag.name)
        else:
            fb = f"ILLEGAL MOVE by {ag.name}: {direction} into non-walkable tile."
            ag.prev_action_plan = fb
            self.add_message(fb)

        # quick relationship tweak
        sl = speech.lower()
        for other in self.agents:
            if other is not ag and other.name.lower() in sl:
                ag.update_relationship(other, 5)

    # ---------------------------------------------------------------- main step
    def step(self):
        now = self.time_manager.advance()
        self.step_count += 1
        self.update_daily_plans(now)                 # daily plans get *no* directives

        # -------- list of texts still alive ---------
        current_dir = [d["text"] for d in self.overseer_directives]

        with ThreadPoolExecutor(max_workers=len(self.agents)) as tp:
            tp.map(lambda a: self.update_agent(a, now, current_dir), self.agents)

        # -------- decrement TTL and purge ----------
        for d in self.overseer_directives:
            d["ttl"] -= 1
        self.overseer_directives = [d for d in self.overseer_directives if d["ttl"] > 0]

    # ---------------------------------------------------------------- rendering
    def render_agents(self, canvas, tile_size: int,
                      sprite_map: dict[str, "tk.PhotoImage"]):
        name_fnt   = tkFont.Font(family="Pixellari", size=8)

        for ag in self.agents:
            cx = ag.x * tile_size + tile_size // 2
            cy = ag.y * tile_size + tile_size // 2

            # sprite or fallback circle
            sprite = sprite_map.get(ag.name)
            if sprite:
                canvas.create_image(cx, cy, image=sprite,
                                    anchor="center", tags="agent_layer")
            else:
                r = tile_size // 3
                canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                   fill="red", tags="agent_layer")

            # name with outline
            name_y = cy + tile_size // 2 + 4
            for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
                canvas.create_text(cx+dx, name_y+dy, text=ag.name,
                                   fill="black", font=name_fnt,
                                   tags="agent_layer")
            canvas.create_text(cx, name_y, text=ag.name,
                               fill="white", font=name_fnt,
                               tags="agent_layer")