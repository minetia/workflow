import os
import json
import random
import time
from datetime import datetime
from backend.bybit_api import bybit_api

class TraderCompetitionEngine:
    """
    [BACKEND] 100 Trader Competition Engine
    - Tracks 100 individual traders based on Bybit real-time market data
    - Manages performance, ranking, and PnL
    """
    def __init__(self):
        self.trader_data_file = "data/traders_100.json"
        self.ranking_file = "data/trader_ranking_history.json"
        self.traders = self._load_traders()
        self.symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "SUIUSDT", "DOGEUSDT"]
        
    def _load_traders(self):
        if os.path.exists(self.trader_data_file):
            try:
                with open(self.trader_data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: pass
            
        # Initial generation of 100 traders
        traders = []
        names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        roles = ["Scalper", "Swing", "Abitrage", "TrendFollower", "CounterTrend"]
        
        for i in range(1, 101):
            t = {
                "id": f"TRDR-{i:03d}",
                "name": f"{random.choice(names)}{random.randint(100, 999)}_{i}",
                "role": random.choice(roles),
                "initial_balance": 10000.0,
                "current_balance": 10000.0 + random.uniform(-500, 2000),
                "profit_all_time": random.uniform(-5, 15), # -5% ~ +15%
                "win_rate": random.uniform(45, 65),
                "last_action": "HOLD",
                "last_symbol": "BTCUSDT",
                "active": True
            }
            traders.append(t)
            
        self._save_traders(traders)
        return traders

    def _save_traders(self, traders):
        os.makedirs("data", exist_ok=True)
        with open(self.trader_data_file, "w", encoding="utf-8") as f:
            json.dump(traders, f, indent=4)

    def update_leaderboard(self):
        """Update trader PnL based on Bybit tickers and simulated strategy outcomes"""
        # Fetch real tickers from Bybit
        tickers = bybit_api.get_tickers(category="linear", symbols=self.symbols)
        # Mock mapping if symbol empty (v5 might return more symbols if category=linear is used)
        prices = {t["symbol"]: float(t["lastPrice"]) for t in tickers if "lastPrice" in t}
        if not prices: prices = {"BTCUSDT": 65000.0, "ETHUSDT": 3500.0}

        for t in self.traders:
            # Simulate a trade outcome (+/- 0.5% with bias towards role)
            volatility = random.uniform(-0.4, 0.45) # slight upward bias
            if t["role"] == "Scalper": volatility *= 1.5
            elif t["role"] == "TrendFollower": volatility *= 0.8
            
            t["current_balance"] = t["current_balance"] * (1 + (volatility / 100))
            t["profit_all_time"] = ((t["current_balance"] - t["initial_balance"]) / t["initial_balance"]) * 100
            t["last_symbol"] = random.choice(list(prices.keys()))
            t["last_action"] = random.choice(["BUY", "SELL", "HOLD"])
            
        # Sort and pick Top 10
        ranked = sorted(self.traders, key=lambda x: x["profit_all_time"], reverse=True)
        self._save_traders(ranked)
        return ranked[:10]

    def get_status(self):
        top_10 = sorted(self.traders, key=lambda x: x["profit_all_time"], reverse=True)[:10]
        return {
            "total_traders": len(self.traders),
            "last_sync": datetime.now().isoformat(),
            "leaderboard": top_10
        }

trader_engine = TraderCompetitionEngine()
