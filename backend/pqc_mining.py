import random
from datetime import datetime

class PQCMiningEngine:
    def __init__(self, engine):
        self.engine = engine

    def mine(self, agent_name, amount):
        ledger = self.engine.ledger
        self.engine.transfer.simulate_lattice_signature(f"mining_{agent_name}_{amount}")
        
        data = ledger.load_state()
        if data["wallets"]["EMPIRE_TREASURY"]["balance"] < amount:
            return {"success": False, "msg": "Treasury empty"}

        efficiency = self.engine.quantum_speed * random.uniform(0.98, 1.02)
        amount *= efficiency
        
        # 🚀 Level-Based Mining Bonus
        wallet_level = data["wallets"].get(agent_name, {}).get("level", 1)
        bonus_map = {1: 1.0, 2: 1.05, 3: 1.15, 4: 1.30}
        bonus = bonus_map.get(wallet_level, 1.0)
        amount *= bonus
        
        # 🏛️ Imperial Tax Calculation
        try:
            from Empire.Governance.Imperial_Tax_Office import imperial_tax_office
            tax_amount, rate, rank, reduction = imperial_tax_office.calculate_tax(agent_name, amount)
            ledger.log(f"🏛️ [Tax Office] {agent_name} Rank: {rank} | Rate: {rate*100:.1f}% ({reduction:.1f}% Discount Applied)")
        except Exception as e:
            # Fallback to base tax if office is unavailable
            tax_amount = amount * 0.10
            ledger.log(f"⚠️ [Tax Office] 연동 실패, 기본 세율 10% 적용. (Error: {e})")

        net_amount = amount - tax_amount

        # Hook to Phoenix Vault
        try:
            from backend.phoenix_vault import phoenix_vault
            phoenix_vault.process_pqc_settlement(tax_amount)
        except: pass

        data["wallets"]["EMPIRE_TREASURY"]["balance"] -= amount
        if agent_name not in data["wallets"]:
            addr = ledger.generate_address(f"{agent_name}_{random.random()}")
            data["wallets"][agent_name] = {"balance": 0.0, "address": addr}
            data["address_book"][addr] = agent_name

        data["wallets"][agent_name]["balance"] += net_amount
        data["circulating_supply"] += net_amount

        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        mk = now.strftime("%Y-%m-%d %H:%M")
        
        history = data.setdefault("mining_history", {})
        if history.get("last_reset_date") != today_str:
            history["total_mined_today"] = 0.0
            history["last_reset_date"] = today_str

        history.setdefault("by_minute", {})[mk] = history["by_minute"].get(mk, 0) + amount
        history["total_mined_today"] += amount
        history["last_mined_amount"] = amount
        history.setdefault("by_region", {})[agent_name] = history.get("by_region", {}).get(agent_name, 0) + amount

        
        ledger.save_state(data)
        ledger.log(f"⛏️ [MINED] {agent_name} | {amount:.4f} PQC")
        return {"success": True, "minted": net_amount}

    def get_stats(self):
        self.engine.rwa.stabilize_price()
        data = self.engine.ledger.load_state()
        history = data.get("mining_history", {})
        minutes = sorted(list(history.get("by_minute", {}).keys()))[-20:]
        chart = [{"time": m.split()[1], "amount": round(history["by_minute"][m], 4)} for m in minutes]
        
        return {
            "pqc_price": round(self.engine.pqc_price_krw, 2),
            "circulating": round(data["circulating_supply"], 2),
            "network_speed": round(self.engine.quantum_speed, 2),
            "treasury": round(data["wallets"]["EMPIRE_TREASURY"]["balance"], 2),
            "target_price": round(self.engine.target_price, 2),
            "last_mined": round(history.get("last_mined_amount", 0.0), 4),
            "total_today": round(history.get("total_mined_today", 0.0), 2),
            "minute_chart": chart,
            "total_supply": data["total_supply"],
            "region_stats": {k: round(v, 2) for k, v in history.get("by_region", {}).items() if "NODE" in k}
        }
