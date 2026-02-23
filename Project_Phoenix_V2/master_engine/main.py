import requests
import pyupbit
import json
from datetime import datetime

# 1. 주군의 전령(송봇) 설정
TELEGRAM_TOKEN = "8555519110:AAFr6gKhN-t-dIfsU9_4f1zeaV-35bELkYM"
TELEGRAM_CHAT_ID = "1107103330"

# 2. 주군의 8대 정찰 종목
MY_COINS = ["BTC", "XRP", "ETH", "DOGE", "SOL", "ZRX", "ONDO", "SUI"]

def send_telegram_report(message):
    """주군의 스마트폰으로 정밀 보고서를 출력합니다."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"출력 오류: {e}")

def run_phoenix_engine():
    """웹 동기화 및 상세 텔레그램 보고 엔진"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scout_results = []
    
    # 보고서 머리말
    report = f"🦅 **Project Phoenix V2 정밀 정찰 보고**\n"
    report += f"------------------------------------\n"
    report += f"📅 **일시**: {now}\n"
    report += f"🛡️ **상태**: 웹 동기화 및 등락 감시 중\n"
    report += f"------------------------------------\n"
    report += f"💰 **실시간 시세 및 등락 (+- %)**\n"

    for coin in MY_COINS:
        try:
            ticker = f"KRW-{coin}"
            price = pyupbit.get_current_price(ticker)
            
            # 전일 대비 등락률 계산
            df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
            prev_close = df.iloc[-2]['close']
            rate = ((price - prev_close) / prev_close) * 100
            
            # 이모지 및 부호 설정
            emoji = "🚀" if rate > 0 else "📉" if rate < 0 else "➡️"
            plus_minus = "+" if rate > 0 else ""
            
            # 가격 포맷팅 (100원 미만 소수점 유지)
            price_fmt = f"{price:,.2f}" if price < 100 else f"{price:,.0f}"
            
            # 텔레그램용 텍스트 추가
            report += f"• **{coin:<5}**: {price_fmt} KRW ({emoji} {plus_minus}{rate:.2f}%)\n"
            
            # 웹 대시보드용 데이터 저장 준비
            scout_results.append({"name": coin, "price": price, "rate": rate})
        except:
            report += f"• **{coin:<5}**: 정찰 지연 중\n"

    report += f"------------------------------------\n"
    report += f"주군, 웹 대시보드와 텔레그램 동기화 완료! 🫡"

    # 웹 대시보드용 데이터(data.json) 저장
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"last_update": now, "coins": scout_results}, f, ensure_ascii=False, indent=4)
    
    # 텔레그램 최종 출력
    send_telegram_report(report)

if __name__ == "__main__":
    run_phoenix_engine()
