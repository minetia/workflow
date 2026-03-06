# File: C:\lovesoong\Castle_5_Management\Imperial_Server_v10000.py
# Role: Imperial Persistent Data Bridge (v10,000)
# Authorized by ServerMaster_MD [cite: 2026-02-28]

from flask import Flask, jsonify, send_from_directory
import os
import json

app = Flask(__name__)
# 상위 루트 경로 계산 (C:\lovesoong)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

@app.route('/')
def index():
    """사령관 전용 대시보드 서빙"""
    return send_from_directory(os.path.join(ROOT_DIR, "Castle_5_Management"), "imperial_dashboard.html")

@app.route('/api/pulse')
def get_pulse():
    """jCollector의 실시간 박동 데이터를 브라우저에 전송"""
    try:
        pulse_path = os.path.join(ROOT_DIR, "logs", "live_pulse.json")
        if os.path.exists(pulse_path):
            with open(pulse_path, "r", encoding="utf-8") as f:
                return jsonify(json.load(f))
        return jsonify({"status": "Waiting for Pulse..."})
    except Exception as e:
        return jsonify({"status": "Error", "msg": str(e)})

if __name__ == "__main__":
    print("-" * 50)
    print("[WebMagician] Asset-linked logic is active.")
    print("[System] Imperial Server v10,000 is now ONLINE.")
    print(f"[Link] Dashboard: http://127.0.0.1:5000")
    print("-" * 50)
    print("!!! 주의: 이 창을 닫으면 대시보드 연결이 끊어집니다 !!!")
    
    # 서버 영구 가동 (debug=False 권장)
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)