# Project_Phoenix_V2/master_engine/main.py
import requests
import pyupbit
from datetime import datetime

# 1. 주군의 전령(송봇) 설정
TELEGRAM_TOKEN = "8555519110:AAFr6gKhN-t-dIfsU9_4f1zeaV-35bELkYM"
TELEGRAM_CHAT_ID = "1107103330"

def send_telegram_report(message):
    """주군의 텔레그램으로 최종 결과물을 출력합니다."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": message, 
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"출력 오류: {e}")

def get_market_snapshot():
    """공용 데이터를 활용한 현재 시장 시세 정찰"""
    try:
        btc_price = pyupbit.get_current_price("KRW-BTC")
        eth_price = pyupbit.get_current_price("KRW-ETH")
        sol_price = pyupbit.get_current_price("KRW-SOL")
        return {
            "BTC": btc_price,
            "ETH": eth_price,
            "SOL": sol_price
        }
    except:
        return None

def run_output_engine():
    """최종 보고서 생성 및 출력 엔진"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    prices = get_market_snapshot()
    
    # 보고서 마크다운 양식 구성
    report = f"🦅 **Project Phoenix V2 시장 정찰 보고**\n"
    report += f"------------------------------------\n"
    report += f"📅 **일시**: {now}\n"
    report += f"🛡️ **상태**: 시스템 정상 가동 중\n"
    report += f"------------------------------------\n"
    report += f"📊 **실시간 주요 종목 시세**\n"
    
    if prices:
        report += f"• **BTC**: {prices['BTC']:,.0f} KRW\n"
        report += f"• **ETH**: {prices['ETH']:,.0f} KRW\n"
        report += f"• **SOL**: {prices['SOL']:,.0f} KRW\n"
    else:
        report += f"⚠️ 데이터 수집 일시적 지연 중\n"
        
    report += f"------------------------------------\n"
    report += f"주군, 현재 전선은 이상 없습니다!\n"
    report += f"다음 명령을 대기하겠습니다. 🫡"
    
    # 텔레그램 출력 실행
    send_telegram_report(report)

if __name__ == "__main__":
    run_output_engine()
