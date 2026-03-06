import os
import json
import random
import time
from datetime import datetime
from backend.bybit_api import bybit_api

class BybitLiveSpeculativeEngine:
    """
    [BACKEND] Bybit Live Speculative Engine (v7)
    - Manages 100 high-frequency traders speculating on real Bybit ticker movements.
    - Generates vivid order books, trade history, and individual PnL snapshots.
    """
    def __init__(self):
        self.traders_file = "data/bybit_traders_live.json"
        self.market_history_file = "data/bybit_market_history.json"
        self.traders = self._init_traders()
        self.symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "SUIUSDT", "ORDIUSDT", "1000PEPEUSDT", "DOGEUSDT"]
        self.order_book = {"bids": [], "asks": []}
        self.trade_history = []

    def _init_traders(self):
        if os.path.exists(self.traders_file):
            try:
                with open(self.traders_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: pass
        
        traders = []
        strategies = ["Aggressive Scalper", "HFT Arbitrage", "Momentum Whale", "Grid Bot", "News Sniper"]
        for i in range(1, 101):
            traders.append({
                "id": f"BYT-{i:03d}",
                "name": f"WOLVE_{random.randint(10,99)}_{i}",
                "strategy": random.choice(strategies),
                "equity": 50000.0,
                "pnl_24h": 0.0,
                "win_count": 0,
                "loss_count": 0,
                "is_active": True,
                "position": {"side": "None", "size": 0, "entry": 0}
            })
        self._save_traders(traders)
        return traders

    def _save_traders(self, traders):
        os.makedirs("data", exist_ok=True)
        with open(self.traders_file, "w", encoding="utf-8") as f:
            json.dump(traders, f, indent=4)

    def synchronize_reality(self):
        """Fetch REAL Bybit data and force 100 traders to react instantly"""
        tickers = bybit_api.get_tickers(category="linear", symbols=self.symbols)
        if not tickers: return
        
        # Pick the most active one for the main view
        main_ticker = tickers[0]
        curr_price = float(main_ticker.get("lastPrice", 0))
        symbol = main_ticker.get("symbol", "BTCUSDT")
        
        # 1. Update Order Book Simulation (centered around real price)
        self.order_book = {
            "bids": [[round(curr_price * (1 - (i*0.0001)), 2), round(random.uniform(0.1, 5.0), 3)] for i in range(1, 15)],
            "asks": [[round(curr_price * (1 + (i*0.0001)), 2), round(random.uniform(0.1, 5.0), 3)] for i in range(1, 15)]
        }
        
        # 2. Force Traders to Trade
        active_trades = []
        for t in self.traders:
            if random.random() > 0.85: # 15% chance to open/close per sync
                action = random.choice(["BUY", "SELL"])
                size = round(random.uniform(0.01, 2.0), 4)
                
                # Update PnL logic
                if t["position"]["side"] != "None":
                    profit = (curr_price - t["position"]["entry"]) if t["position"]["side"] == "BUY" else (t["position"]["entry"] - curr_price)
                    t["equity"] += profit * t["position"]["size"]
                    t["pnl_24h"] = ((t["equity"] - 50000.0) / 50000.0) * 100
                    if profit > 0: t["win_count"] += 1
                    else: t["loss_count"] += 1
                
                t["position"] = {"side": action, "size": size, "entry": curr_price}
                active_trades.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "trader": t["name"],
                    "side": action,
                    "price": curr_price,
                    "size": size
                })
        
        self.trade_history = (active_trades + self.trade_history)[:30]
        self._save_traders(self.traders)
        
        return {
            "symbol": symbol,
            "price": curr_price,
            "change": main_ticker.get("price24hPcnt", "0.00"),
            "order_book": self.order_book,
            "history": self.trade_history,
            "top_traders": sorted(self.traders, key=lambda x: x["pnl_24h"], reverse=True)[:10]
        }

bybit_live_engine = BybitLiveSpeculativeEngine()
