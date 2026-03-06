# File: jCollector_Realtime_Pro.py
# Role: Imperial Real-time Data Harvester (v10,000)
# Authorized by ServerMaster_MD [cite: 2026-02-28]

import os
import time
import json
import requests
from datetime import datetime

class jCollector_MD:
    def __init__(self):
        self.name = "[jCollector_MD]"
        self.target = "BTC/USDT"
        self.api_url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

    def fetch_live_market(self):
        """실제 거래소 API에서 비트코인 시세를 수집 [cite: 2026-02-13]"""
        try:
            response = requests.get(self.api_url, timeout=5)
            data = response.json()
            price = float(data['price'])
            return price
        except Exception as e:
            print(f"{self.name} Sensor Error: {e}")
            return None

    def broadcast_to_empire(self, price):
        """수집된 데이터를 제국 통합 로그(live_pulse.json)에 전송"""
        log_path = "./logs/live_pulse.json"
        pulse_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "btc_price": price,
            "status": "LIVE_SYNCED",
            "commander": "최송학 (Choi Song-hag)", #
            "location": "Gumi, KR" #
        }
        
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(pulse_data, f, ensure_ascii=False, indent=4)
        print(f"{self.name} Pulse Transmitted: ${price:,.2f}")

    def run_perpetual_scan(self):
        print(f"{self.name} v10,000 Real-time Sensor Engaged.")
        while True:
            price = self.fetch_live_market()
            if price:
                self.broadcast_to_empire(price)
            time.sleep(1) # 1초 단위 고속 스캔 [cite: 2026-02-13]

if __name__ == "__main__":
    Collector = jCollector_MD()
    Collector.run_perpetual_scan()