# -*- coding: utf-8 -*-
"""
[설명: PHOENIX_ENGINE_V10 - 통합 실행 지휘소]
사령관님이 하달하신 6개의 잼을 유기적으로 연결하여 실전 매매를 수행한다.
"""
from modules.collector_jam import CollectorJam
from modules.strategist_jam import StrategistJam
from modules.guardian_jam import RiskGuardianJam
from modules.allocator_jam import CapitalAllocatorJam
from modules.sniper_jam import SniperJam
from modules.executor_jam import ExecutorJam

class PhoenixTradingEngine:
    def __init__(self):
        # 6인 참모진 소환
        self.collector = CollectorJam()
        self.strategist = StrategistJam()
        self.guardian = RiskGuardianJam()
        self.allocator = CapitalAllocatorJam(total_balance=100000000) # 1억 원 세팅
        self.sniper = SniperJam()
        self.executor = ExecutorJam()

    def run_cycle(self):
        print("\n⚡ [Engine] 제국 트레이딩 사이클 가동...")
        
        # 1. 수집 (Collector)
        data = self.collector.collect_all(asset="BTC")
        
        # 2. 분석 (Strategist)
        decision = self.strategist.analyze(data)
        if decision['action'] == "HOLD":
            print("💤 [Engine] 관망 유지. 다음 사이클을 대기합니다.")
            return

        # 3. 리스크 평가 (Guardian)
        risk_report = self.guardian.assess_risk(data)
        if risk_report['action'] == "ABORT":
            print("🚨 [Engine] 리스크 초과! 거래를 중단합니다.")
            return

        # 4. 자금 배분 (Allocator)
        alloc = self.allocator.calculate_size(risk_report['risk_score'], data['price'])
        
        # 5. 타점 정밀 계산 (Sniper)
        strike_point = self.sniper.get_entry_point(decision['asset'], data['price'], decision)

        # 6. 최종 실행 (Executor)
        result = self.executor.execute(decision, strike_point['target_price'], alloc['position_size'], risk_report['risk_score'])
        
        print(f"🏆 [Engine] 사이클 종료: {result['execution_status']} | 수익을 기록합니다.")

if __name__ == "__main__":
    engine = PhoenixTradingEngine()
    engine.run_cycle()