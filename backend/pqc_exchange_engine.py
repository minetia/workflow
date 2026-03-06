import sys
import os

# Ensure global dependencies can be resolved
BASE_DIR = r"c:\lovesoong"
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from backend.matching_engine import MatchingEngine
from backend.quantum_coin_engine import pqc_engine

class PQCExchangeEngine(MatchingEngine):
    """
    제국 PQC 거래소 엔진: 각 성단과 중앙 허브에서 공통으로 사용하는 고성능 매칭 엔진.
    """
    def __init__(self, exchange_name):
        super().__init__()
        self.exchange_name = exchange_name
        self.save_path = os.path.join(BASE_DIR, "data", f"{exchange_name}_trades.json")
        
        # Ensure data directory exists
        data_dir = os.path.dirname(self.save_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        self.load_trades()

    def run_cycle(self):
        """거래소 사이클 실행: 대기 중인 주문 매칭 및 상태 보고"""
        book = self.get_order_book()
        print(f"🏛️ [{self.exchange_name} Exchange] Market Active.")
        if book['buys']:
            print(f"  > High Bid: {book['buys'][0]['price']} PQC")
        if book['sells']:
            print(f"  > Low Ask: {book['sells'][0]['price']} PQC")
        return book

# Create specific instances as needed
if __name__ == "__main__":
    # Test instance
    test_ex = PQCExchangeEngine("TEST")
    test_ex.run_cycle()
