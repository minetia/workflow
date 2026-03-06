import sys
import os

# Ensure global dependencies can be resolved
BASE_DIR = r"c:\lovesoong"
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from backend.quantum_coin_engine import pqc_engine
import time

class QuantumMiningCentralCommand:
    """
    제국 양자 채굴 중앙 사령부: 전 국가(Alpha, Core, Nexus, Zion)의 PQC 채굴을 총괄 관리.
    양자 컴퓨터 자원을 배분하고 전역 원장(Global Ledger)을 실시간으로 업데이트.
    """
    def __init__(self):
        self.engine = pqc_engine

    def orchestrate_mining(self):
        """전 국가 채굴 상태 점검 및 중앙 보고"""
        stats = self.engine.get_mining_stats()
        print(f"🔱 [양자 중앙 사령부] 제국 양자 컴퓨터 가동 중 (Network Speed: {stats['network_speed']})")
        print(f"💰 [양자 중앙 사령부] 현재 PQC 유통량: {stats['circulating']} PQC")
        print(f"🏛️ [양자 중앙 사령부] 제국 국고 잔액: {stats['treasury']} PQC")
        return stats

    def receive_mining_report(self, nation, amount):
        """각 성단으로부터 채굴 결과 수신 및 기록"""
        result = self.engine.mine_pqc(f"CASTLE_{nation.upper()}", amount)
        if result["success"]:
            print(f"✅ [양자 중앙 사령부] {nation} 성단으로부터 {amount} PQC 채굴 보고 수신 및 승인.")
        return result

# Global Instance
quantum_central_command = QuantumMiningCentralCommand()
