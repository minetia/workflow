import requests
import pyupbit
import json # 추가
from datetime import datetime

TELEGRAM_TOKEN = "8555519110:AAFr6gKhN-t-dIfsU9_4f1zeaV-35bELkYM"
TELEGRAM_CHAT_ID = "1107103330"
MY_COINS = ["BTC", "XRP", "ETH", "DOGE", "SOL", "ZRX", "ONDO", "SUI"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})

def run_scout():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scout_results = []
    report = f"🦅 **Phoenix V2 웹 동기화 완료**\n"
    
    for coin in MY_COINS:
        ticker = f"KRW-{coin}"
        price = pyupbit.get_current_price(ticker)
        df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
        rate = ((price - df.iloc[-2]['close']) / df.iloc[-2]['close']) * 100
        
        scout_results.append({"name": coin, "price": price, "rate": rate})
        report += f"• {coin}: {rate:+.2f}%\n"

    # 웹 대시보드용 데이터 저장
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump({"last_update": now, "coins": scout_results}, f, ensure_ascii=False, indent=4)
    
    send_telegram(report + f"\n주군, 웹 대시보드가 갱신되었습니다.")

if __name__ == "__main__":
    run_scout()
