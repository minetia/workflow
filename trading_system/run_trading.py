# -*- coding: utf-8 -*-
import sys
import os
import time

# =================================================================
# [STEP 1] 지도 펼치기 (Path Configuration)
# 이 작업이 모든 import보다 '무조건' 먼저 실행되어야 합니다.
# =================================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = r"c:\lovesoong"

# Add national sectors to sys.path for dependencies
paths_to_add = [
    os.path.join(base_dir, "Zion"),   # For PHOENIX_CIVITAS
    os.path.join(base_dir, "Empire"), # For PHOENIX_HUB
    current_dir                        # For local modules
]

for p in paths_to_add:
    if p not in sys.path:
        sys.path.append(p)

# =================================================================
# [STEP 2] 요원 소환 (Imports)
# 이제 파이썬이 지도를 가졌으므로, 모든 폴더의 요원을 부를 수 있습니다.
# =================================================================
try:
    from PHOENIX_CIVITAS.panopticon_logic import PhoenixPanopticon
    from PHOENIX_HUB.telegram_bot import PhoenixMessenger
    from modules.collector_jam import CollectorJam
    from modules.strategist_jam import StrategistJam
    from modules.guardian_jam import RiskGuardianJam
    from modules.allocator_jam import CapitalAllocatorJam
    from modules.sniper_jam import SniperJam
    from modules.executor_jam import ExecutorJam
    print("✅ [System] 모든 참모진이 작전실에 집결했습니다.")
except ImportError as e:
    print(f"🚨 [Error] 요원 소환 실패: {e}")
    sys.exit(1)

# =================================================================
# [STEP 3] 제국 엔진 본체 (Engine Logic)
# =================================================================
class PhoenixImperialEngine:
    def __init__(self):
        self.name = "PHOENIX_IMPERIAL_V10"
        self.panopticon = PhoenixPanopticon()
        self.messenger = PhoenixMessenger()
        self.collector = CollectorJam()
        self.strategist = StrategistJam()
        self.guardian = RiskGuardianJam()
        self.allocator = CapitalAllocatorJam()
        self.sniper = SniperJam()
        self.executor = ExecutorJam()

    def run_mission(self):
        print(f"🎯 [{self.name}] 시장 사냥을 시작합니다.")
        self.messenger.send_message("⚔️ *제국 통합 엔진 가동. 관제 센터 동기화 완료!*")

        while True:
            try:
                # 1. 수집 -> 2. 분석 -> 3. 방어 -> 4. 타격 -> 5. 보고
                data = self.collector.collect_all()
                decision = self.strategist.analyze(data)
                
                # 관제 센터 데이터 업데이트
                self.panopticon.update_live_view(data, "HUNTING", 0)

                if decision['action'] != "HOLD":
                    risk = self.guardian.assess_risk(data)
                    alloc = self.allocator.calculate_size(risk['risk_score'], data['price'])
                    strike = self.sniper.get_entry_point("BTC", data['price'], decision)
                    result = self.executor.execute(decision, strike['target_price'], alloc['position_size'], risk['risk_score'])
                    
                    if result.get('status') == "SUCCESS":
                        # 수익 보고서 발송 (Messenger)
                        self.messenger.send_message(f"💰 *수익 기회 포착!*\n자산: {result['asset']}\n상태: 체결 완료")

                time.sleep(60) # 1분마다 순찰
            except Exception as e:
                print(f"🚨 엔진 일시 오류: {e}")
                time.sleep(10)

if __name__ == "__main__":
    engine = PhoenixImperialEngine()
    engine.run_mission()