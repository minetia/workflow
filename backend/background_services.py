import time
import random
import subprocess
import threading
import os
from trading_system.modules.collector_jam import CollectorJam
from trading_system.modules.strategist_jam import StrategistJam
from trading_system.modules.sniper_jam import SniperJam
from trading_system.modules.guardian_jam import RiskGuardianJam
from trading_system.modules.allocator_jam import CapitalAllocatorJam
from trading_system.modules.executor_jam import ExecutorJam
from backend.quantum_coin_engine import pqc_engine

def phoenix_quantum_loop():
    collector = CollectorJam()
    strategist = StrategistJam()
    sniper = SniperJam()
    guardian = RiskGuardianJam()
    allocator = CapitalAllocatorJam()
    executor = ExecutorJam()

    print("\n🦅 [System] PHOENIX V10 기동 부대(The 6 Jams) 가동 준비 완료. 시장 감시를 시작합니다.\n")

    while True:
        try:
            raw_data = collector.collect_all(asset="BTC")
            decision = strategist.analyze(raw_data)
            
            if decision.get('action') in ["BUY", "SELL"]:
                target = sniper.get_entry_point(decision.get('asset'), raw_data.get('price'), decision)
                risk_check = guardian.assess_risk(raw_data)
                
                if risk_check.get('status') == "SAFE":
                    allocation = allocator.calculate_size(risk_check.get('risk_score'), target.get('target_price'))
                    if allocation.get('position_size', 0) > 0:
                        execution_report = executor.execute(decision, target.get('target_price'), allocation.get('position_size'), risk_check.get('risk_score'))
                        print(f"✅ [JAM SUCCESS] 체결 보고서: {execution_report}")
                    else:
                        print("⚠️ [Allocator] 할당할 투입 자금이 없습니다.")
                else:
                    print(f"🚫 [Guardian] 시장 위험 감지. 주문 차단됨 (사유: {risk_check.get('status')})")
            
            # ⚡ PERF: 10s → 45s to drastically reduce CPU/API call pressure
            time.sleep(45)
        except Exception as e:
            print(f"❌ [JAM ERROR] 기동 부대 루프 중 오류 발생: {e}")
            time.sleep(15)

def phoenix_mining_loop():
    """제국 PQC 채굴 부대의 무한 채굴 루프"""
    print("⛏️ [System] PHOENIX Mining Loop: ACTIVE. Quantum resources being extracted...")
    agents = ["KOR_NODE", "USA_NODE", "JPN_NODE", "EU_NODE"]
    while True:
        try:
            agent = random.choice(agents)
            amount = random.uniform(1.2, 5.8)
            pqc_engine.mine_pqc(agent, amount)
            # ⚡ PERF: 5-12s → 30-60s to reduce IO and thread pressure
            time.sleep(random.randint(15, 30))
        except Exception as e:
            print(f"❌ [MINING ERROR] 채굴 중 오류 발생: {e}")
            time.sleep(15)

def phoenix_surveyor_loop():
    """제국 영토 감시 루프: 5분마다 신규 폴더 스캔 및 제국루트.txt 갱신"""
    try:
        from backend.empire_surveyor import empire_surveyor
        print("🛰️ [System] PHOENIX Surveyor: ACTIVE. Monitoring territorial expansions...")
        while True:
            try:
                result = empire_surveyor.scan_and_update()
                if result.get('added', 0) > 0:
                    print(f"📍 [Surveyor] New expansion recorded: {result['added']} territories added to Route Map.")
                time.sleep(300) # 5분 간격
            except Exception as e:
                print(f"❌ [SURVEYOR ERROR] 영토 감시 루프 내부 오류 발생: {e}")
                time.sleep(60)
    except Exception as e:
        print(f"❌ [SURVEYOR CRITICAL] 모듈 로드 실패: {e}")

def start_community_relay():
    """커뮤니티 소셜 통신망 가동 (Separate Process)"""
    try:
        print("🌐 [System] Starting Community Relay Server on port 5050...")
        subprocess.Popen(["python", "COMMUNITY_SQUARE/community_server.py"], 
                         cwd="C:/Users/loves/workflow", 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.STDOUT)
    except Exception as e:
        print(f"❌ [System] Failed to start Community Relay: {e}")

def start_all_services(imperial_backup, auto_promotion_loop, bridge_monitor_loop, scanner_monitor_loop):
    """지휘관 전용 통합 백그라운드 서비스 기동 매니저"""
    print("\n👑 [PHOENIX] Starting Collective Background Services...")
    
    # 1. Core Trading & Mining Loops
    threading.Thread(target=phoenix_quantum_loop, daemon=True).start()
    threading.Thread(target=phoenix_mining_loop, daemon=True).start()
    threading.Thread(target=phoenix_surveyor_loop, daemon=True).start()
    start_community_relay()

    # 2. Infrastructure Loops (Passed from main)
    # ⚡ PERF: backup interval 3s → 60s (was consuming constant IO)
    imperial_backup.start_monitoring(interval=60)
    threading.Thread(target=auto_promotion_loop, daemon=True).start()
    threading.Thread(target=bridge_monitor_loop, daemon=True).start()
    threading.Thread(target=scanner_monitor_loop, daemon=True).start()
    
    print("✅ All background services synchronized.\n")
