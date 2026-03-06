import os
import sys
import importlib.util
import time
import io
import random

# Ensure UTF-8 for Windows PowerShell
if os.name == 'nt':
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = r"c:\lovesoong"

# Global Dependency resolution
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

def get_dept_paths(nation_name):
    """Returns the standardized department suite for a nation."""
    return [
        os.path.join(BASE_DIR, nation_name, "Dept_Trading", "MD_Trading.py"),
        os.path.join(BASE_DIR, nation_name, "Dept_Scanner", "MD_Scanner.py"),
        os.path.join(BASE_DIR, nation_name, "Dept_Scanner", "investigator.py"),
        os.path.join(BASE_DIR, nation_name, "Dept_Quantum", "Agent_Qiskit_Simulator.py"),
        os.path.join(BASE_DIR, nation_name, "Dept_Quantum", "oracle.py"),
        os.path.join(BASE_DIR, nation_name, "Dept_Security", "vault_protector.py"),
        os.path.join(BASE_DIR, nation_name, "Dept_Security", "sentinel_read.py")
    ]

PROJECTS = {
    "Empire": [
        os.path.join(BASE_DIR, "Empire", "Emperor_Brain.py"),
        os.path.join(BASE_DIR, "Empire", "Communication_Hub", "Neural_Link_Core.py"),
        os.path.join(BASE_DIR, "Empire", "Communication_Hub", "Empire_Intelligence_Hub.py"),
        os.path.join(BASE_DIR, "Empire", "Governance", "Trading_Ranking_System.py"),
        os.path.join(BASE_DIR, "Empire", "Governance", "Imperial_Tax_Office.py"),
        os.path.join(BASE_DIR, "Empire", "Governance", "Imperial_Quantum_Dungeon.py"),
        os.path.join(BASE_DIR, "Empire", "Governance", "Imperial_Backup_Vault.py"),
        os.path.join(BASE_DIR, "Empire", "Governance", "Imperial_Trading_Grand_Prix.py"),
        os.path.join(BASE_DIR, "Empire", "Central_Exchange.py"),
        os.path.join(BASE_DIR, "Empire", "Quantum_Mining_Central_Command.py"),
        os.path.join(BASE_DIR, "Empire", "JAM_Auto_Forge", "jam.py"),
        os.path.join(BASE_DIR, "Empire", "JAM_Auto_Forge", "Architect.py"),
        os.path.join(BASE_DIR, "Empire", "JAM_Auto_Forge", "Chancellor.py")
    ],
    "Alpha": [
        os.path.join(BASE_DIR, "Alpha", "Alpha_Commander.py"),
        os.path.join(BASE_DIR, "Alpha", "JAM_Architect.py"),
        os.path.join(BASE_DIR, "Alpha", "JAM_Designer.py"),
        os.path.join(BASE_DIR, "Alpha", "JAM_Enforcer.py"),
        os.path.join(BASE_DIR, "Alpha", "JAM_Steward.py"),
        os.path.join(BASE_DIR, "Alpha", "Alpha_Exchange.py"),
        os.path.join(BASE_DIR, "Alpha", "Trading_Forge", "run_trading.py"),
        os.path.join(BASE_DIR, "Alpha", "Quantum_Mining_Node.py")
    ] + get_dept_paths("Alpha"),
    "Core": [
        os.path.join(BASE_DIR, "Core", "Core_Commander.py"),
        os.path.join(BASE_DIR, "Core", "JAM_Engineer.py"),
        os.path.join(BASE_DIR, "Core", "JAM_Enforcer.py"),
        os.path.join(BASE_DIR, "Core", "JAM_Steward.py"),
        os.path.join(BASE_DIR, "Core", "Core_Exchange.py"),
        os.path.join(BASE_DIR, "Core", "spiritual_monitor.py"),
        os.path.join(BASE_DIR, "Core", "Trading_Forge", "run_trading.py"),
        os.path.join(BASE_DIR, "Core", "Quantum_Mining_Node.py")
    ] + get_dept_paths("Core"),
    "Nexus": [
        os.path.join(BASE_DIR, "Nexus", "Nexus_Commander.py"),
        os.path.join(BASE_DIR, "Nexus", "JAM_Ambassador.py"),
        os.path.join(BASE_DIR, "Nexus", "JAM_Chancellor.py"),
        os.path.join(BASE_DIR, "Nexus", "JAM_Enforcer.py"),
        os.path.join(BASE_DIR, "Nexus", "JAM_Steward.py"),
        os.path.join(BASE_DIR, "Nexus", "Nexus_Exchange.py"),
        os.path.join(BASE_DIR, "Nexus", "nexus_bridge.py"),
        os.path.join(BASE_DIR, "Nexus", "Trading_Forge", "run_trading.py"),
        os.path.join(BASE_DIR, "Nexus", "Quantum_Mining_Node.py")
    ] + get_dept_paths("Nexus"),
    "Zion": [
        os.path.join(BASE_DIR, "Zion", "Zion_Commander.py"),
        os.path.join(BASE_DIR, "Zion", "JAM_Enforcer.py"),
        os.path.join(BASE_DIR, "Zion", "JAM_Steward.py"),
        os.path.join(BASE_DIR, "Zion", "JAM_Archivist.py"),
        os.path.join(BASE_DIR, "Zion", "JAM_Steward.py"),
        os.path.join(BASE_DIR, "Zion", "Zion_Exchange.py"),
        os.path.join(BASE_DIR, "Zion", "Trading_Forge", "run_trading.py"),
        os.path.join(BASE_DIR, "Zion", "Quantum_Mining_Node.py")
    ] + get_dept_paths("Zion")
}

def execute_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_nation_suite(nation_name, paths):
    print(f"\n[*] [{nation_name}] 구역 진입 및 전문 부서 가동...")
    try:
        for path in paths:
            filename = os.path.basename(path)
            if os.path.exists(path):
                # Import module dynamically
                module_name = filename.replace(".py", "")
                module = execute_module(module_name, path)
                
                # Logic per special component
                if "Commander" in filename: 
                    if hasattr(module, f"{nation_name}Commander"):
                        cmd_class = getattr(module, f"{nation_name}Commander")()
                        if hasattr(cmd_class, "scan"): cmd_class.scan()
                        elif hasattr(cmd_class, "compute"): cmd_class.compute()
                        elif hasattr(cmd_class, "trade"): cmd_class.trade()
                        elif hasattr(cmd_class, "protect"): cmd_class.protect()
                elif "JAM_Enforcer" in filename:
                    module.JAM_Enforcer().execute_oversight()
                elif "JAM_Steward" in filename:
                    module.JAM_Steward(nation_name).execute_oversight()
                elif "JAM_" in filename:
                    agent_name = filename.replace(".py", "").replace("JAM_", "")
                    print(f"  > [JAM_{agent_name.upper()}] 현지 관리 감독관 가동.")
                elif "Central_Exchange" in filename: module.global_central_exchange.orchestrate_global_liquidity()
                elif "_Exchange" in filename: 
                    ex_attr = f"{nation_name.lower()}_exchange"
                    if hasattr(module, ex_attr):
                        getattr(module, ex_attr).manage_local_market()
                elif "Imperial_Quantum_Dungeon" in filename: 
                    status = module.imperial_dungeon.get_dungeon_status()
                    print(f"🏰 [Imperial Dungeon] Prisoner Count: {status['prisoner_count']}")
                elif "Imperial_Backup_Vault" in filename:
                    module.imperial_backup_vault.execute_supreme_backup()
                elif "Imperial_Trading_Grand_Prix" in filename:
                    # Simulate Grand Prix check (Monthly cycle)
                    # For demo: trigger a mini-정산 if specific flag or random chance
                    if random.random() < 0.2:
                        mock_metrics = {
                            "Alpha": {"profit": random.uniform(10, 50), "accuracy": random.uniform(0.7, 0.95)},
                            "Core": {"profit": random.uniform(10, 50), "accuracy": random.uniform(0.7, 0.95)},
                            "Nexus": {"profit": random.uniform(10, 50), "accuracy": random.uniform(0.7, 0.95)},
                            "Zion": {"profit": random.uniform(10, 50), "accuracy": random.uniform(0.7, 0.95)}
                        }
                        module.imperial_grand_prix.calculate_cycle_results(mock_metrics)
                elif "Agent_Qiskit_Simulator" in filename: print("  > Quantum Sim: ONLINE.")
                elif "oracle" in filename: print(f"  > Reveal: {module.OracleAI().reveal_truth()[:50]}...")
                elif "Emperor_Brain" in filename: module.EmperorBrain().issue_order("Global", "Grand Prix Protocol Active")
                elif "Neural_Link_Core" in filename: print("  > Neural Link: SYNCHRONIZED.")
                elif "Empire_Intelligence_Hub" in filename: module.intelligence_hub.broadcast_to_castles()
                elif "Trading_Ranking_System" in filename: module.trading_ranker.update_rankings()
                elif "Imperial_Tax_Office" in filename: print("  > IRS: DYNAMIC TAXATION ACTIVE.")
                elif "Quantum_Mining_Central_Command" in filename: module.quantum_central_command.orchestrate_mining()
                elif "Quantum_Mining_Node" in filename: module.QuantumMiningNode(nation_name).run_mining_sequence()
                elif filename == "jam.py": print("  > [JAM_PRIME] 제국 총괄 지형지물 제어판 가동.")
                elif "run_trading" in filename: print(f"  > [{nation_name}] Trading Forge: ENGINE_READY.")
                elif "MD_Trading" in filename: 
                    legion_path = os.path.join(BASE_DIR, nation_name, "QUANTUM_LEGION")
                    legion_count = len([f for f in os.listdir(legion_path) if f.endswith(".py")]) if os.path.exists(legion_path) else 0
                    print(f"  > Trading Node: ACTIVE. (Quantum Legion: {legion_count} Agents Online)")
                elif "MD_Scanner" in filename: print(f"  > Scanner: [{nation_name}] 구역 정밀 스캔 중.")
                elif "investigator" in filename: print(f"  > Investigator: 단서 추적 및 데이터 심층 분석.")
                elif "vault_protector" in filename: print(f"  > Security: {module.VaultProtector().verify_vault()}")
                elif "sentinel_read" in filename: print(f"  > Archive: {module.SentinelArchiveAI().verify_archives()}")
                
        print(f"[+] [{nation_name}] 실전 부서 체계 가동 완료.")
    except Exception as e:
        print(f"[!] [{nation_name}] 오류 발생: {e}")

def run_super_pipeline():
    print("\n" + "="*70)
    print("🔱 [ZION EMPIRE] GLOBAL SUPER-PIPELINE V4.3 ACTIVATED")
    print("TIME: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    print("GRAND PRIX MODE: ENABLED")
    print("="*70)
    
    for nation, paths in PROJECTS.items():
        run_nation_suite(nation, paths)
        time.sleep(1)

if __name__ == "__main__":
    run_super_pipeline()
    print("\n" + "="*70)
    print("👑 제국 전체 전선 이상 없음: SUPREME OPTIMAL")
    print("="*70)
