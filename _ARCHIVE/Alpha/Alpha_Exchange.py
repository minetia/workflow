from backend.pqc_exchange_engine import PQCExchangeEngine

class AlphaExchange(PQCExchangeEngine):
    def __init__(self):
        super().__init__("Alpha_Regional")

    def manage_local_market(self):
        print("🏛️ [Alpha Exchange] Managing local market liquidity.")
        return self.run_cycle()

alpha_exchange = AlphaExchange()
