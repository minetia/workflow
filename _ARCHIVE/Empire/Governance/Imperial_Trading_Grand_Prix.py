import os
import json
import random
from datetime import datetime

BASE_DIR = r"c:\lovesoong"

class ImperialTradingGrandPrix:
    """
    🏆 [IMPERIAL TRADING GRAND PRIX] - 제국 트레이딩 대전람회
    매달 최고의 수익률과 기술을 보여준 성단을 선별하고, 엘리트 인재를 중앙으로 소환합니다.
    """
    def __init__(self):
        self.history_file = os.path.join(BASE_DIR, "data", "grand_prix_history.json")
        self.elites_file = os.path.join(BASE_DIR, "data", "scouted_elites.json")
        self.history = self._load_data(self.history_file)
        self.elites = self._load_data(self.elites_file)

    def _load_data(self, path):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return [] if "history" in path else {}
        return [] if "history" in path else {}

    def _save_data(self, path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def calculate_cycle_results(self, castle_metrics):
        """
        한 달 주기의 대회 결과를 정산합니다.
        castle_metrics: {castle_name: {"profit": float, "accuracy": float}}
        """
        cycle_id = datetime.now().strftime("%Y-%m")
        print(f"🏆 [GrandPrix] {cycle_id} 사이클 최종 정산 개시...")
        
        # Scoring logic
        results = []
        for castle, data in castle_metrics.items():
            score = (data["profit"] * 0.7) + (data["accuracy"] * 30)
            results.append({"castle": castle, "score": round(score, 2), "profit": data["profit"]})
        
        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        winner = results[0]
        
        # Prize distribution (PQC + Recognition)
        prize = winner["profit"] * 0.1 # 10% bonus
        print(f"🥇 우승 성단: {winner['castle']} (Score: {winner['score']})")
        print(f"💰 포상: {round(prize, 4)} PQC 지급 및 차기 달 세금 감면 혜택 부여.")
        
        # Elite Scouting logic: 
        # In a real system, this would move a specific JAM or user.
        # Here we record the "Champion" status.
        scouted_agent = f"JAM_ELITE_{winner['castle']}_{random.randint(100, 999)}"
        self.elites[cycle_id] = {
            "origin": winner["castle"],
            "agent": scouted_agent,
            "achievement": f"ITGP {cycle_id} Champion"
        }
        
        self.history.append({
            "cycle": cycle_id,
            "winner": winner["castle"],
            "scouted": scouted_agent,
            "stats": results
        })
        
        self._save_data(self.history_file, self.history)
        self._save_data(self.elites_file, self.elites)
        
        return winner

    def get_hall_of_fame(self):
        return self.elites

# Global Instance
imperial_grand_prix = ImperialTradingGrandPrix()
