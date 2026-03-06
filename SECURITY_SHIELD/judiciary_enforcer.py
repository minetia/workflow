import json
import os
import random
import time
from datetime import datetime

class JudiciaryEnforcer:
    def __init__(self):
        self.log_file = "SYSTEM_LOGS/judiciary.log"
        self.agent_file = "data/agents.json"
        
        self._ensure_files()
        
    def _ensure_files(self):
        os.makedirs("SYSTEM_LOGS", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.agent_file):
            # Seed with some initial data based on earlier context if file missing
            default_agents = [
                {"id": "USR-001", "nickname": "Alex_TraderPRO", "title": "MASTER", "status": "ACTIVE", "points": 50000, "roi": 12.4},
                {"id": "BLD-88F1", "nickname": "Omega", "title": "OPERATIVE", "status": "ACTIVE", "points": 5000, "roi": -3.2},
                {"id": "USR-003", "nickname": "CryptoWhale_99", "title": "NOVICE", "status": "ACTIVE", "points": 1000, "roi": -15.0}
            ]
            with open(self.agent_file, "w", encoding="utf-8") as f:
                json.dump(default_agents, f, indent=4)

    def _log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {msg}\n")
        print(f"[JUDICIARY] {msg}")

    def execute_judgment(self):
        """Scans agents and punishes those with terrible RoI or rule violations."""
        with open(self.agent_file, "r", encoding="utf-8") as f:
            agents = json.load(f)
            
        punishments = []
        for agent in agents:
            # Simulate slight continuous ROI changes from the invisible market
            agent["roi"] = agent.get("roi", 0.0) + random.uniform(-2.0, 1.5)
            
            if agent["status"] in ["EXECUTED", "DEACTIVATED"]:
                continue
                
            if agent["roi"] <= -10.0 and agent["status"] == "ACTIVE":
                agent["status"] = "PUNISHED"
                penalty = agent["points"] * 0.5
                agent["points"] -= penalty
                msg = f"WARNING: {agent['nickname']} pushed to PUNISHED. Penalty: {penalty:.0f} PTS (RoI: {agent['roi']:.1f}%)"
                self._log(msg)
                punishments.append(msg)
                
            elif agent["roi"] <= -20.0 and agent["status"] == "PUNISHED":
                agent["status"] = "EXECUTED"
                agent["points"] = 0
                msg = f"💀 EXECUTION: {agent['nickname']} has been EXECUTED by the Judiciary for critical failure (RoI: {agent['roi']:.1f}%)."
                self._log(msg)
                punishments.append(msg)
                
        with open(self.agent_file, "w", encoding="utf-8") as f:
            json.dump(agents, f, indent=4)
            
        return punishments

judiciary_enforcer = JudiciaryEnforcer()

def judiciary_monitor_loop():
    """Background thread to run the judiciary judgments"""
    while True:
        try:
            judiciary_enforcer.execute_judgment()
        except:
            pass
        time.sleep(15) # Judgments passed every 15 seconds
