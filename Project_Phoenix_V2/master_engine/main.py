import requests
import pyupbit
from datetime import datetime

# 1. 주군의 전령(송봇) 설정
TELEGRAM_TOKEN = "8555519110:AAFr6gKhN-t-dIfsU9_4f1zeaV-35bELkYM"
TELEGRAM_CHAT_ID = "1107103330"

# 2. 주군의 8가지 정찰 종목 (BTC, XRP, ETH, DOGE, SOL, ZRX, ONDO, SUI)
MY_COINS = ["BTC", "XRP", "ETH", "DOGE", "SOL", "ZRX", "ONDO", "SUI"]

def send_telegram_report(message):
    """주군의 텔레그램으로 전황 보고서를 출력합니다."""
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

def run_scout_engine():
    """지정된 8개 종목의 실시간 시세를 수집 및 보고합니다."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = f"🦅 **Project Phoenix V2 실시간 전황 보고**\n"
    report += f"------------------------------------\n"
    report += f"📅 **일시**: {now}\n"
    report += f"🛡️ **상태**: 8대 종목 정찰 중\n"
    report += f"------------------------------------\n"
    report += f"💰 **주군 지정 종목 현재가**\n"

    for coin in MY_COINS:
        try:
            ticker = f"KRW-{coin}"
            price = pyupbit.get_current_price(ticker)
            if price:
                # 100원 이하는 소수점 2자리, 이상은 정수로 표시
                if price < 100:
                    report += f"• **{coin:<5}**: {price:,.2f} KRW\n"
                else:
                    report += f"• **{coin:<5}**: {price:,.0f} KRW\n"
            else:
                report += f"• **{coin:<5}**: 시세 확인 불가\n"
        except:
            report += f"• **{coin:<5}**: 연결 지연\n"

    report += f"------------------------------------\n"
    report += f"주군, 8명의 전사들이 전선에서 대기 중입니다! 🫡"
    
    send_telegram_report(report)

if __name__ == "__main__":
    run_scout_engine()
