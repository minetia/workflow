import json
import os
import random
import time
from datetime import datetime
from backend.indicator_engine import indicator_engine

class ExchangeBridge:
    def __init__(self):
        self.log_file = "SYSTEM_LOGS/exchange_bridge.log"
        self.orders_file = "data/active_orders.json"
        self.market_file = "data/mock_market_prices.json"
        
        # Security: Load API keys securely from environment variables (Server-side only)
        # Prevents API Key leakage even if source code is exposed.
        self.upbit_api_key = os.environ.get("UPBIT_API_KEY", "MOCK_SECURE_KEY_88F1")
        self.upbit_secret_key = os.environ.get("UPBIT_SECRET_KEY", "MOCK_SECRET_XYZ_999")
        
        # Available tradeable pairs
        self.pairs = ["BTC-KRW", "ETH-KRW", "SOL-KRW", "XRP-KRW", "DOGE-KRW"]
        
        self._ensure_files()
        
    def _ensure_files(self):
        os.makedirs("SYSTEM_LOGS", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.orders_file):
            with open(self.orders_file, "w") as f:
                json.dump([], f)
        if not os.path.exists(self.market_file):
            with open(self.market_file, "w") as f:
                json.dump({p: random.uniform(100, 100000000) for p in self.pairs}, f)

    def _log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {msg}\n")
        print(f"[EXCHANGE] {msg}")

    def update_market_prices(self):
        """Randomly fluctuate prices by small percentages (-2% to +2%)"""
        with open(self.market_file, "r") as f:
            prices = json.load(f)
            
        for pair in prices:
            change = random.uniform(-0.02, 0.02)
            prices[pair] = prices[pair] * (1 + change)
            
        with open(self.market_file, "w") as f:
            json.dump(prices, f, indent=4)
        return prices

    def execute_trades_from_signals(self):
        """Translates indicator_engine signals into simulated mock exchange orders"""
        state = indicator_engine.get_live_processing_state()
        market_prices = self.update_market_prices()
        
        with open(self.orders_file, "r") as f:
            history = json.load(f)
            
        new_orders = []
        for agent_data in state["live_compute"]:
            agent_name = agent_data["agent"]
            
            # Count Buys vs Sells to determine final action
            buy_power = sum([1 for p in agent_data["processing"] if p["signal"] == "BUY"])
            sell_power = sum([1 for p in agent_data["processing"] if p["signal"] == "SELL"])
            
            # If strong majority, execute trade
            if buy_power >= 3:
                pair = random.choice(self.pairs)
                order = {
                    "id": f"ORD-{random.randint(10000, 99999)}",
                    "agent": agent_name,
                    "action": "BUY",
                    "pair": pair,
                    "price_krw": market_prices[pair],
                    "volume": round(float(random.uniform(0.1, 5.0)), 4),
                    "timestamp": datetime.now().isoformat(),
                    "status": "FILLED"
                }
                new_orders.append(order)
                self._log(f"🟢 [BUY FIRED] {agent_name} bought {order['volume']} {pair} @ {order['price_krw']:.0f}KRW. Reason: Strong technical aggregation.")
                
            elif sell_power >= 3:
                pair = random.choice(self.pairs)
                order = {
                    "id": f"ORD-{random.randint(10000, 99999)}",
                    "agent": agent_name,
                    "action": "SELL",
                    "pair": pair,
                    "price_krw": market_prices[pair],
                    "volume": round(float(random.uniform(0.1, 5.0)), 4),
                    "timestamp": datetime.now().isoformat(),
                    "status": "FILLED"
                }
                new_orders.append(order)
                self._log(f"🔴 [SELL FIRED] {agent_name} sold {order['volume']} {pair} @ {order['price_krw']:.0f}KRW. Reason: Strong technical aggregation.")
                
        # Append and keep last 100
        history.extend(new_orders)
        history = history[-100:]
        
        with open(self.orders_file, "w") as f:
            json.dump(history, f, indent=4)
            
        return {
            "success": True,
            "orders_fired": len(new_orders),
            "latest_prices": market_prices
        }

exchange_bridge = ExchangeBridge()

def bridge_monitor_loop():
    """Background thread to run the exchange (SIMULATION DISABLED)"""
    while True:
        try:
            # exchange_bridge.execute_trades_from_signals() # DISABLED: No more fake trades
            pass
        except Exception as e:
            pass
        time.sleep(30) # Check every 30s instead of 10s
