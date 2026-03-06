import json
import os
from datetime import datetime

from pathlib import Path

class HubManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.registry_file = self.base_dir / "data" / "exchange_registry.json"
        self._ensure_registry()
        
    def _ensure_registry(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.registry_file):
            # Default template for major exchanges
            initial_data = {
                "Domestic": {
                    "Upbit": {"BTC": "", "ETH": "", "XRP": "", "SOL": "", "KRW": ""},
                    "Bithumb": {"BTC": "", "ETH": "", "XRP": "", "SOL": "", "KRW": ""},
                    "Coinone": {"BTC": "", "ETH": "", "XRP": "", "SOL": "", "KRW": ""}
                },
                "Overseas": {
                    "Binance": {"BTC": "", "ETH": "", "XRP": "", "SOL": "", "ZRX": "", "ONDO": ""},
                    "Coinbase": {"BTC": "", "ETH": "", "XRP": "", "SOL": ""},
                    "Bybit": {"BTC": "", "ETH": "", "SOL": "", "SUI": ""}
                },
                "last_updated": datetime.now().isoformat()
            }
            with open(self.registry_file, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=4)

    def get_registry(self):
        try:
            with open(self.registry_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            self._ensure_registry()
            with open(self.registry_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        # Reality Sync: Generate addresses for empty fields
        modified = False
        try:
            from backend.quantum_coin_engine import pqc_engine
            for category in ["Domestic", "Overseas"]:
                if category in data:
                    cat_items = data.get(category, {})
                    if isinstance(cat_items, dict):
                        for exchange, coins in cat_items.items():
                            if isinstance(coins, dict):
                                for coin, addr in coins.items():
                                    # Detect empty, short, or invalid strings
                                    if not isinstance(addr, str) or not addr or len(addr) < 8 or "시 " in addr:
                                        new_addr = pqc_engine.ledger.generate_address(f"{exchange}_{coin}", coin, "REAL")
                                        coins[coin] = new_addr
                                        modified = True
        except Exception as e:
            print(f"Hub Reality Sync Error: {e}")
        
        if modified:
            data["last_updated"] = datetime.now().isoformat()
            try:
                with open(self.registry_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
            except: pass
                
        return data

    def update_address(self, category, exchange, coin, address):
        data = self.get_registry()
        if category in data and exchange in data[category]:
            data[category][exchange][coin] = address
            data["last_updated"] = datetime.now().isoformat()
            with open(self.registry_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return {"success": True, "message": f"{exchange} {coin} 주소가 업데이트되었습니다."}
        return {"success": False, "message": "유효하지 않은 거래소 또는 카테고리입니다."}

hub_manager = HubManager()
