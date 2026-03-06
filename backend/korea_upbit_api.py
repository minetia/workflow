"""
[BACKEND] Upbit Core API Bridge
- Wraps internal Upbit API logic for the Phoenix Empire Main Engine
"""
import os
import json

class UpbitCore:
    def __init__(self):
        self.access_key = None
        self.secret_key = None
        self.config_file = "data/upbit_config.json"
        self._load_config()
    def _load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                    self.access_key = config.get("access_key")
                    self.secret_key = config.get("secret_key")
            except:
                pass

    def set_keys(self, access, secret):
        self.access_key = access
        self.secret_key = secret
        os.makedirs("data", exist_ok=True)
        with open(self.config_file, "w") as f:
            json.dump({"access_key": access, "secret_key": secret}, f)

    def _build_token(self, query=None):
        """JWT 인증 토큰 생성"""
        if not self.access_key or not self.secret_key:
            return ""
        import jwt
        import uuid
        import hashlib
        payload = {
            "access_key": self.access_key,
            "nonce": str(uuid.uuid4()),
        }
        if query:
            query_str = "&".join(f"{k}={v}" for k, v in query.items())
            m = hashlib.sha512()
            m.update(query_str.encode())
            payload["query_hash"] = m.hexdigest()
            payload["query_hash_alg"] = "SHA512"

        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return f"Bearer {token}"

    def get_accounts(self):
        """실제 Upbit 잔고 조회"""
        import httpx
        token = self._build_token()
        if not token: return []
        
        try:
            resp = httpx.get("https://api.upbit.com/v1/accounts", headers={"Authorization": token}, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except: pass
        return []

    def get_ticker(self, markets):
        """실제 실시간 시세 조회"""
        import httpx
        market_str = ",".join(markets)
        try:
            resp = httpx.get("https://api.upbit.com/v1/ticker", params={"markets": market_str}, timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except: pass
        return []

upbit_core = UpbitCore()
