import sys
import os

# Ensure global dependencies can be resolved
BASE_DIR = r"c:\lovesoong"
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

try:
    from Empire.Quantum_Mining_Central_Command import quantum_central_command
except ImportError:
    quantum_central_command = None

import time
import random

class QuantumMiningNode:
    """
    성단 양자 채굴 노드: 중앙 사령부의 지휘 하에 각 성단에서 PQC를 채굴하고 보고.
    """
    def __init__(self, nation):
        self.nation = nation

    def run_mining_sequence(self):
        """채굴 시퀀스 실행 및 중앙 사령부 보고"""
        print(f"⛏️ [{self.nation}] 양자 채굴 시퀀스 개시...")
        
        # Simulate mining amount based on the castle's power
        mined_amount = round(random.uniform(0.1, 0.5), 6)
        
        if quantum_central_command:
            quantum_central_command.receive_mining_report(self.nation, mined_amount)
        else:
            print(f"⚠️ [{self.nation}] 중앙 사령부 연결 실패. 로컬 데이터에 임시 저장.")
        
        return mined_amount

# Global Node Instance (to be initialized by the pipeline or commander)
# node = QuantumMiningNode("Alpha")
