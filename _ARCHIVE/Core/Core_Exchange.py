from backend.pqc_exchange_engine import PQCExchangeEngine

class CoreExchange(PQCExchangeEngine):
    def __init__(self):
        super().__init__("Core_Regional")

    def manage_local_market(self):
        print("🏛️ [Core Exchange] Managing local market liquidity.")
        return self.run_cycle()

core_exchange = CoreExchange()
