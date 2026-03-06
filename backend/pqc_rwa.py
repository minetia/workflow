import random

class PQCRWAEngine:
    def __init__(self, engine):
        self.engine = engine

    def stabilize_price(self):
        dev = (self.engine.pqc_price_krw - self.engine.target_price) / self.engine.target_price
        self.engine.quantum_speed = min(5.0, self.engine.quantum_speed + 0.05) if abs(dev) < 0.02 else max(0.1, self.engine.quantum_speed - 0.1)
        self.engine.pqc_price_krw *= (1 - 0.05 * dev + random.uniform(-0.001, 0.001))
        if dev < -0.05: self.execute_buyback()
        return self.engine.pqc_price_krw

    def execute_buyback(self):
        self.engine.pqc_price_krw *= 1.015
        self.engine.ledger.log("🛡️ [TREASURY] Floor Support active. Buyback deployed.")

    def issue_physical_rwa(self, wallet_name, amount):
        ledger = self.engine.ledger
        self.engine.gateway.synchronize()
        data = ledger.load_state()
        if wallet_name not in data["wallets"] or data["wallets"][wallet_name]["balance"] < amount:
            return {"success": False, "msg": "Insufficient"}
        gold_cost = amount * 0.0001
        if self.engine.gold_backed_reserve_kg < gold_cost:
            return {"success": False, "msg": "Gold reserve insufficient"}
        data["wallets"][wallet_name]["balance"] -= amount
        data["burned_supply"] += amount
        self.engine.gold_backed_reserve_kg -= gold_cost
        ledger.save_state(data)
        return {"success": True, "gold": gold_cost}
