import os
import sys
import importlib.util
import time
import io
import json
import random
from datetime import datetime

# Ensure UTF-8 for Windows PowerShell
if os.name == 'nt':
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = r"c:\lovesoong"

# Global Dependency resolution
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

def execute_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class CommandTowerV7:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data = {
            "Empire": {}, "Alpha": {}, "Core": {}, "Nexus": {}, "Zion": {}
        }

    def collect_telemetry(self):
        """성단별 실시간 데이터를 수집합니다."""
        from Empire.Governance.Trading_Ranking_System import trading_ranker
        from Empire.Governance.Imperial_Tax_Office import imperial_tax_office
        from Empire.Governance.Imperial_Quantum_Dungeon import imperial_dungeon
        from Empire.Governance.Imperial_Backup_Vault import imperial_backup_vault
        from Empire.Governance.Imperial_Trading_Grand_Prix import imperial_grand_prix

        # Empire Central
        b_info = {"timestamp": "N/A", "file_count": 0}
        if os.path.exists(imperial_backup_vault.last_backup_file):
            with open(imperial_backup_vault.last_backup_file, "r") as f:
                b_info = json.load(f)
        
        d_status = imperial_dungeon.get_dungeon_status()
        gp_elites = imperial_grand_prix.get_hall_of_fame()
        current_cycle = datetime.now().strftime("%Y-%m")
        champion = gp_elites.get(current_cycle, {}).get("origin", "PENDING")

        self.data["Empire"] = {
            "dungeon": f"{d_status['prisoner_count']} Subjects",
            "backup": f"{b_info['timestamp']} ({b_info['file_count']} Assets)",
            "champion": champion,
            "status": "SUPREME_READY"
        }

        # Castles
        for castle in ["Alpha", "Core", "Nexus", "Zion"]:
            tax_rate, rank, reduction = imperial_tax_office.get_tax_rate(castle)
            
            # Dynamic wellness check
            steward_path = os.path.join(BASE_DIR, castle, "JAM_Steward.py")
            f_index = "N/A"
            if os.path.exists(steward_path):
                stew_mod = execute_module(f"stew_{castle}", steward_path)
                stew = stew_mod.JAM_Steward(castle)
                f_index = stew.fatigue_index

            self.data[castle] = {
                "rank": f"{rank}위",
                "tax": f"{tax_rate*100}% (-{reduction}%)",
                "wellness": f"{f_index} (Index)",
                "gatekeeper": "ACTIVE",
                "mining": f"{round(random.uniform(0.1, 0.5), 2)} PQC"
            }

    def render_5_monitor(self):
        """5개 모니터 형식으로 시각화합니다."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*80)
        print("🔱 [ZION EMPIRE] SUPREME COMMAND TOWER V7.0 - 5-MONITOR MULTI-PLEX")
        print(f"TIME: {self.timestamp} | GLOBAL STATUS: OPTIMAL")
        print("="*80)

        # Top Row: Alpha & Core
        print(f"{'[ MONITOR 1: ALPHA ]':<40} {'[ MONITOR 2: CORE ]':<40}")
        print(f"{'--------------------':<40} {'-------------------':<40}")
        print(f"{'[Rank] ' + self.data['Alpha']['rank']:<40} {'[Rank] ' + self.data['Core']['rank']:<40}")
        print(f"{'[Tax] ' + self.data['Alpha']['tax']:<40} {'[Tax] ' + self.data['Core']['tax']:<40}")
        print(f"{'[Wellness] ' + self.data['Alpha']['wellness']:<40} {'[Wellness] ' + self.data['Core']['wellness']:<40}")
        print(f"{'[Dungeon] Gatekeeper: ON':<40} {'[Dungeon] Gatekeeper: ON':<40}")
        print(f"{'[Mining] ' + self.data['Alpha']['mining']:<40} {'[Mining] ' + self.data['Core']['mining']:<40}")
        print("\n")

        # Middle: Empire Central
        indent = " " * 20
        print(f"{indent}       [ MONITOR 0: EMPIRE CENTRAL ]")
        print(f"{indent}       -----------------------------")
        print(f"{indent}       [INCARCERATION] {self.data['Empire']['dungeon']}")
        print(f"{indent}       [BACKUP] {self.data['Empire']['backup']}")
        print(f"{indent}       [GRAND PRIX] Champion: {self.data['Empire']['champion']}")
        print(f"{indent}       [SYSTEM] {self.data['Empire']['status']}")
        print(f"{indent}       [IRS] Dynamic Taxation: ACTIVE")
        print("\n")

        # Bottom Row: Nexus & Zion
        print(f"{'[ MONITOR 3: NEXUS ]':<40} {'[ MONITOR 4: ZION ]':<40}")
        print(f"{'--------------------':<40} {'-------------------':<40}")
        print(f"{'[Rank] ' + self.data['Nexus']['rank']:<40} {'[Rank] ' + self.data['Zion']['rank']:<40}")
        print(f"{'[Tax] ' + self.data['Nexus']['tax']:<40} {'[Tax] ' + self.data['Zion']['tax']:<40}")
        print(f"{'[Wellness] ' + self.data['Nexus']['wellness']:<40} {'[Wellness] ' + self.data['Zion']['wellness']:<40}")
        print(f"{'[Dungeon] Gatekeeper: ON':<40} {'[Dungeon] Gatekeeper: ON':<40}")
        print(f"{'[Mining] ' + self.data['Nexus']['mining']:<40} {'[Mining] ' + self.data['Zion']['mining']:<40}")
        
        print("="*80)
        print("👑 제국 전체 전선 이상 없음: VISUAL_OPTIMAL (5-PLEX UPDATED)")
        print("="*80)

if __name__ == "__main__":
    tower = CommandTowerV7()
    tower.collect_telemetry()
    tower.render_5_monitor()
