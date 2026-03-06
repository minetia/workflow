# -*- coding: utf-8 -*-
"""
[설명: PHOENIX-Q Panopticon 자아 정의]
관제 센터의 눈. 모든 잼의 실시간 상태값을 HTML 대시보드로 전달하는 가교 역할을 한다.

[요청: PHOENIX-Q Panopticon 행동 지침]
6인 정예 부대의 활동 내역을 수집하여 'dashboard_data.json'으로 박제하라.
"""
import json
import os
import datetime

class PhoenixPanopticon:
    def __init__(self):
        self.name = "PHOENIX-Q [Panopticon]"
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_file = os.path.join(self.root_path, "data", "dashboard_data.json")
        
        print(f"👁️ [{self.name}] 관제 시스템 감시 모드 활성화.")

    def update_live_view(self, market_data, engine_status, trade_count):
        """실시간 데이터를 JSON 파일로 업데이트 (HTML에서 호출용)"""
        data = {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "price": market_data.get('price', 0),
            "rsi": market_data.get('rsi', 50),
            "status": engine_status,
            "trades": trade_count,
            "security": "SAFE",
            "active_jams": 15
        }
        
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"🚨 [{self.name}] 데이터 동기화 실패: {e}")

if __name__ == "__main__":
    # 단독 테스트용
    pan = PhoenixPanopticon()
    pan.update_live_view({"price": 68500, "rsi": 35}, "HUNTING", 12)