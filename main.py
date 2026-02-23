from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pyupbit
import asyncio
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# [1] 이미지에서 정밀 추출한 사용자 포트폴리오 (로그인 불필요)
MY_PORTFOLIO = [
    {"code": "KRW-ZRX",  "name": "제로엑스",   "qty": 39624.97820587, "avg": 357.1},
    {"code": "KRW-BTC",  "name": "비트코인",   "qty": 0.02012913,     "avg": 139647010},
    {"code": "KRW-ETH",  "name": "이더리움",   "qty": 0.61347396,     "avg": 4727629},
    {"code": "KRW-XRP",  "name": "리플",       "qty": 552.06964239,   "avg": 2913.0},
    {"code": "KRW-SOL",  "name": "솔라나",     "qty": 6.99730942,     "avg": 192965},
    {"code": "KRW-SUI",  "name": "수이",       "qty": 522.10839461,   "avg": 2470.3},
    {"code": "KRW-ONDO", "name": "온도파이낸스", "qty": 627.08252377,   "avg": 478.0}
]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # 조회할 티커 리스트 생성 (내 코인 + 달러 환산용 USDT)
    tickers = [item["code"] for item in MY_PORTFOLIO]
    tickers.append("KRW-USDT") 

    while True:
        try:
            # 실시간 현재가 조회 (업비트 Public API - 키 필요없음)
            prices = pyupbit.get_current_price(tickers)
            
            # 환율 계산 (USDT 가격을 달러 환율로 간주)
            usdt_price = prices.get("KRW-USDT", 1400) 
            
            response_data = []

            for coin in MY_PORTFOLIO:
                current_price = prices.get(coin["code"], 0)
                
                # 데이터 계산
                valuation = current_price * coin["qty"]      # 평가금액
                invested = coin["avg"] * coin["qty"]         # 매수금액
                profit = valuation - invested                # 평가손익
                rate = ((current_price - coin["avg"]) / coin["avg"]) * 100 # 수익률
                
                # USD 가격 계산
                usd_price = current_price / usdt_price

                response_data.append({
                    "name": coin["name"],
                    "code": coin["code"].split("-")[1], # ZRX, BTC 등
                    "qty": coin["qty"],
                    "avg": coin["avg"],
                    "cur_price_krw": current_price,
                    "cur_price_usd": usd_price,
                    "valuation": valuation,
                    "invested": invested,
                    "profit": profit,
                    "rate": rate
                })

            # 웹소켓 전송
            await websocket.send_json({
                "type": "update",
                "usdt_rate": usdt_price,
                "data": response_data
            })
            
            await asyncio.sleep(0.5)  # 0.5초마다 갱신 (빠른 속도)

        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)