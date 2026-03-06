import threading
import time
from backend.background_services import phoenix_quantum_loop, phoenix_mining_loop
from backend.exchange_bridge import bridge_monitor_loop
from backend.chart_scanner import scanner_monitor_loop
from backend.auto_promotion import auto_promotion_loop
from backend.imperial_backup import imperial_backup_loop

def start_background_services():
    """🛡️ [PHOENIX-V12] Imperial Service Orchestrator"""
    services = [
        ("QuantumTrading", phoenix_quantum_loop),
        ("MiningEngine", phoenix_mining_loop),
        ("ExchangeBridge", bridge_monitor_loop),
        ("ChartScanner", scanner_monitor_loop),
        ("AutoPromotion", auto_promotion_loop),
        ("ImperialBackup", imperial_backup_loop)
    ]

    for name, loop_func in services:
        thread = threading.Thread(target=loop_func, name=f"PHOENIX_{name}", daemon=True)
        thread.start()
        print(f"✅ [ORCHESTRATOR] {name} service initialized and deployed.")

    print("🚀 [PHOENIX EMPIRE] All background systems are now under Imperial Control.")
