import os
import json
import hmac
import hashlib
import time
import httpx
from datetime import datetime

class BybitRealEngine:
    """
    [BACKEND] Bybit Real Trading Engine (v5)
    - Supports REAL SPOT and LINEAR (Futures/Margin) trading.
    - Handles authentication, order placement, and position management.
    """
    def __init__(self):
        self.config_file = "data/bybit_config.json"
        self.base_url = "https://api.bybit.com" # Mainnet
        self.api_key = ""
        self.api_secret = ""
        self.recv_window = "5000"
        self._load_keys()

    def _load_keys(self):
        # 1. Try Environment Variables first
        self.api_key = os.getenv("BYBIT_API_KEY", "")
        self.api_secret = os.getenv("BYBIT_API_SECRET", "")
        
        # 2. Fallback to config file if env is empty
        if not self.api_key and os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.api_key = config.get("api_key", "")
                    self.api_secret = config.get("api_secret", "")
            except: pass

    def _generate_signature(self, timestamp, payload):
        param_str = timestamp + self.api_key + self.recv_window + payload
        hash = hmac.new(self.api_secret.encode("utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        signature = hash.hexdigest()
        return signature

    def _send_request(self, method, endpoint, params=None):
        if not self.api_key or not self.api_secret:
            return {"retCode": -1001, "retMsg": "API Keys are missing. Please register keys first."}
            
        timestamp = str(int(time.time() * 1000))
        
        # Build payload for signing
        if method == "GET":
            payload = "&".join([f"{k}={v}" for k, v in sorted(params.items())]) if params else ""
            full_url = f"{self.base_url}{endpoint}"
            if payload: full_url += f"?{payload}"
        else: # POST
            payload = json.dumps(params) if params else "{}"
            full_url = f"{self.base_url}{endpoint}"

        signature = self._generate_signature(timestamp, payload)
        
        headers = {
            "X-BAPI-API-KEY": self.api_key,
            "X-BAPI-SIGN": signature,
            "X-BAPI-TIMESTAMP": timestamp,
            "X-BAPI-RECV-WINDOW": self.recv_window,
            "Content-Type": "application/json"
        }
        
        try:
            with httpx.Client() as client:
                if method == "GET":
                    resp = client.get(full_url, headers=headers, timeout=10)
                else:
                    resp = client.post(full_url, headers=headers, data=payload, timeout=10)
                return resp.json()
        except Exception as e:
            return {"retCode": -999, "retMsg": str(e)}

    # --- PUBLIC METHODS ---
    
    def get_wallet_balance(self, accountType="UNIFIED", coins=None):
        """Fetch real wallet balances"""
        params = {"accountType": accountType}
        if coins: params["coin"] = ",".join(coins)
        return self._send_request("GET", "/v5/account/wallet-balance", params)

    def get_positions(self, category="linear", symbol=None):
        """Fetch active futures positions"""
        params = {"category": category}
        if symbol: params["symbol"] = symbol
        return self._send_request("GET", "/v5/position/list", params)

    def place_order(self, category, symbol, side, orderType, qty, price=None, leverage=None, tp=None, sl=None):
        """
        Place Real Order (Spot or Linear)
        - tp: Take Profit Price
        - sl: Stop Loss Price
        """
        # 1. Set Leverage for Futures (Linear) if specified
        if category == "linear" and leverage is not None:
            self.set_leverage(symbol, leverage)

        params = {
            "category": category,
            "symbol": symbol,
            "side": side,
            "orderType": orderType,
            "qty": str(qty),
            "timeInForce": "GTC"
        }
        
        if price: params["price"] = str(price)
        if orderType == "Market": params.pop("price", None)
        
        # Add TP/SL for Futures
        if category == "linear":
            if tp: params["takeProfit"] = str(tp)
            if sl: params["stopLoss"] = str(sl)
            params["isLeverage"] = 1 # Force leverage mode
        
        return self._send_request("POST", "/v5/order/create", params)

    def set_leverage(self, symbol, leverage, category="linear"):
        """Update leverage for a specific symbol"""
        return self._send_request("POST", "/v5/position/set-leverage", {
            "category": category,
            "symbol": symbol,
            "buyLeverage": str(leverage),
            "sellLeverage": str(leverage)
        })

    def close_position(self, category, symbol, side, qty):
        """Close a linear position by placing an opposite market order"""
        opposite_side = "Sell" if side == "Buy" else "Buy"
        return self.place_order(category, symbol, opposite_side, "Market", qty)

    def get_active_orders(self, category="linear", symbol=None):
        params = {"category": category, "openOnly": 0}
        if symbol: params["symbol"] = symbol
        return self._send_request("GET", "/v5/order/realtime", params)

    def cancel_order(self, category, symbol, orderId):
        return self._send_request("POST", "/v5/order/cancel", {
            "category": category,
            "symbol": symbol,
            "orderId": orderId
        })

bybit_real_engine = BybitRealEngine()
