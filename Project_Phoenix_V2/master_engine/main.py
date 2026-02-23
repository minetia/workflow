import pyupbit
import json
import datetime
import os

# 1. 감시할 8대 전사 목록
COINS = ["KRW-BTC", "KRW-XRP", "KRW-ETH", "KRW-DOGE", "KRW-SOL", "KRW-ZRX", "KRW-ONDO", "KRW-SUI"]

def scout_market():
    print("🚀 피닉스 엔진 가동: 시장 데이터 정찰 중...")
    
    # 실시간 시세 가져오기
    current_prices = pyupbit.get_current_price(COINS)
    
    coin_data = []
    for ticker in COINS:
        name = ticker.replace("KRW-", "")
        price = current_prices.get(ticker, 0)
        
        # 전일 대비 등락률 계산 (상세 데이터 가져오기)
        df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
        if df is not None and len(df) >= 2:
            prev_close = df.iloc[0]['close']
            rate = ((price - prev_close) / prev_close) * 100
        else:
            rate = 0.0

        coin_data.append({
            "name": name,
            "price": price,
            "rate": round(rate, 2)
        })

    # data.json 구조 만들기
    report = {
        "last_update": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_balance": 10000000, # 현재는 가상 자산. API 연동 시 실제 잔고로 변경 가능
        "coins": coin_data
    }

    # 최상위 폴더에 data.json 저장
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)
        
    print("✅ data.json 생성 완료!")

if __name__ == "__main__":
    try:
        scout_market()
        # 여기에 주군의 자동매매 로직 (buy/sell)이 추가로 돌아갑니다.
    except Exception as e:
        print(f"❌ 엔진 오류 발생: {e}")
