import requests
import pyupbit
from datetime import datetime

# 1. 주군의 전령(송봇) 설정
TELEGRAM_TOKEN = "8555519110:AAFr6gKhN-t-dIfsU9_4f1zeaV-35bELkYM"
TELEGRAM_CHAT_ID = "1107103330"

# 2. 주군의 8대 정찰 종목
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

def get_coin_data(ticker):
    """현재가와 전일 대비 변동률을 가져옵니다."""
    try:
        # 현재가 가져오기
        current_price = pyupbit.get_current_price(ticker)
        
        # 전일 종가(오늘 시가) 가져와서 변동률 계산
        df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
        prev_close = df.iloc[-2]['close']
        change_rate = ((current_price - prev_close) / prev_close) * 100
        
        return current_price, change_rate
    except:
        return None, None

def run_advanced_scout():
    """변동률이 포함된 정밀 정찰 보고서를 작성합니다."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = f"🦅 **Project Phoenix V2 정밀 정찰 보고**\n"
    report += f"------------------------------------\n"
    report += f"📅 **일시**: {now}\n"
    report += f"🛡️ **상태**: 8대 종목 변동률 감시 중\n"
    report += f"------------------------------------\n"
    report += f"💰 **실시간 시세 및 등락 (전일대비)**\n"

    for coin in MY_COINS:
        ticker = f"KRW-{coin}"
        price, rate = get_coin_data(ticker)
        
        if price is not None and rate is not None:
            # 이모지 결정
            emoji = "🚀" if rate > 0 else "📉" if rate < 0 else "➡️"
            plus_minus = "+" if rate > 0 else ""
            
            # 가격 포맷팅 (100원 미만은 소수점 유지)
            price_fmt = f"{price:,.2f}" if price < 100 else f"{price:,.0f}"
            
            report += f"• **{coin:<5}**: {price_fmt} KRW ({emoji} {plus_minus}{rate:.2f}%)\n"
        else:
            report += f"• **{coin:<5}**: 데이터 수집 실패\n"

    report += f"------------------------------------\n"
    report += f"주군, 전선에서 전사들이 승전보를 기다립니다! 🫡"
    
    send_telegram_report(report)

if __name__ == "__main__":
    run_advanced_scout()
