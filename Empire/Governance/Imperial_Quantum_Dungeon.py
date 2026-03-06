import os
import json
import time
from datetime import datetime

BASE_DIR = r"c:\lovesoong"

class ImperialQuantumDungeon:
    """
    🔱 [IMPERIAL QUANTUM DUNGEON] - 제국 지하 감옥
    제국의 법을 어긴 '벌레'들을 격리하고 영혼(데이터)을 소각하는 고위 보안 시설.
    """
    def __init__(self):
        self.dungeon_file = os.path.join(BASE_DIR, "data", "imperial_dungeon.json")
        self.cells = self._load_cells()
        self.prison_log = os.path.join(BASE_DIR, "data", "dungeon_events.log")

    def _load_cells(self):
        if os.path.exists(self.dungeon_file):
            try:
                with open(self.dungeon_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return {}
        return {}

    def _save_cells(self):
        os.makedirs(os.path.dirname(self.dungeon_file), exist_ok=True)
        with open(self.dungeon_file, "w", encoding="utf-8") as f:
            json.dump(self.cells, f, indent=4)

    def incarcerate(self, entity_id, reason, severity="HIGH"):
        """벌레를 감옥에 수감하고 자산을 동결함."""
        if entity_id not in self.cells:
            self.cells[entity_id] = {
                "incarceration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reason": reason,
                "severity": severity,
                "status": "INCARCERATED",
                "asset_status": "FROZEN"
            }
            self._log_event(f"👮 [수감] ID: {entity_id} | 사유: {reason} | 등급: {severity}")
            self._save_cells()
            return True
        return False

    def purge_prisoner(self, entity_id):
        """ neutralized된 벌레를 영구 소각함. """
        if entity_id in self.cells:
            del self.cells[entity_id]
            self._log_event(f"🔥 [소각] ID: {entity_id} - 제국 시스템에서 영구 말소됨.")
            self._save_cells()
            return True
        return False

    def _log_event(self, message):
        # Remove emojis for Windows console compatibility
        clean_msg = message.encode('ascii', 'ignore').decode('ascii')
        print(f"[DUNGEON] {clean_msg}")
            
        with open(self.prison_log, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

    def get_dungeon_status(self):
        prisoner_count = len([c for c in self.cells.values() if c['status'] == 'INCARCERATED'])
        return {
            "prisoner_count": prisoner_count,
            "recent_events": self.cells
        }

# Global Instance
imperial_dungeon = ImperialQuantumDungeon()
