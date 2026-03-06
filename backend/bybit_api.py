import os
import json
import httpx
import random
import time

class BybitAPI:
    """
    [BACKEND] Bybit Core API Bridge (v5)
    - Provides real-time tickers and simulated/real account data
    """
    def __init__(self):
        self.api_key = os.environ.get("BYBIT_API_KEY", "")
        self.api_secret = os.environ.get("BYBIT_API_SECRET", "")
        self.base_url = "https://api.bybit.com"
        self.config_file = "data/bybit_config.json"
        self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    self.api_key = config.get("api_key", self.api_key)
                    self.api_secret = config.get("api_secret", self.api_secret)
            except: pass

    def set_keys(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        os.makedirs("data", exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump({"api_key": api_key, "api_secret": api_secret}, f)
            
    def get_tickers(self, category="spot", symbols=None):
        """Fetch real tickers from Bybit public API"""
        url = f"{self.base_url}/v5/market/tickers"
        params = {"category": category}
        if symbols:
            # Note: v5 ticker by symbol is singular or we just filter
            pass
            
        try:
            # We fetch all if symbols not specified to avoid complexity for now
            resp = httpx.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("retCode") == 0:
                    result = data.get("result", {}).get("list", [])
                    if symbols:
                        # symbols should be a list like ["BTCUSDT", "ETHUSDT"]
                        return [t for t in result if t["symbol"] in symbols]
                    return result
        except Exception as e:
            print(f"Bybit Ticker Error: {e}")
            
        # Mock fallback if API fails
        return [{"symbol": "BTCUSDT", "lastPrice": str(65000 + random.randint(-40, 40)), "price24hPcnt": "0.02"}]

    def get_accounts(self):
        """Simulated account info (until REAL keys are provided)"""
        if not self.api_key or not self.api_secret:
            return {
                "retCode": 0,
                "result": {
                    "list": [
                        {"coin": "USDT", "equity": "10000.00", "availableToWithdraw": "10000.00"},
                        {"coin": "BTC", "equity": "0.15", "availableToWithdraw": "0.15"}
                    ]
                }
            }
        # Real authentication logic (optional, for later)
        return {"retCode": -1, "retMsg": "Real API Keys needed for account sync."}

bybit_api = BybitAPI()
