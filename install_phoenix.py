import os

print("🔥 [Project Phoenix] 시스템 구축을 시작합니다 (접속 오류 수정판)...")

# ==========================================
# 1. 파일 내용 정의
# ==========================================

files = {}

# [1] 의존성 라이브러리
files["requirements.txt"] = """fastapi
uvicorn
jinja2
python-dotenv
pyupbit
pandas
websockets
"""

# [2] 환경변수 (본인 키 입력 필요)
files[".env"] = """UPBIT_ACCESS_KEY=your_access_key
UPBIT_SECRET_KEY=your_secret_key
TRADE_TICKER=KRW-BTC
"""

files[".gitignore"] = """.env
__pycache__/
*.db
.DS_Store
"""

# [3] 메인 서버 (수정됨: host="127.0.0.1")
files["main.py"] = """from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from core.trader import PhoenixTrader
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

trader = PhoenixTrader()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = trader.get_status()
        await websocket.send_json(data)
        await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(trader.run_loop())
    print("🚀 Phoenix Trader 백그라운드 실행 시작")

if __name__ == "__main__":
    import uvicorn
    # [수정됨] 0.0.0.0 -> 127.0.0.1 (지갑 경고 방지)
    # reload=True 추가 (코드 수정 시 자동 재시작)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
"""

# [4] Core 모듈
files["core/__init__.py"] = ""

files["core/config.py"] = """import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")
TICKER = os.getenv("TRADE_TICKER", "KRW-BTC")
"""

files["core/exchange.py"] = """import pyupbit
from core.config import ACCESS_KEY, SECRET_KEY

class Exchange:
    def __init__(self):
        # 키가 없으면 로그인 없이 시세만 조회하도록 처리
        try:
            self.upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)
        except:
            self.upbit = None

    def get_balance(self, ticker):
        if self.upbit is None: return 0
        try:
            currency = ticker.split('-')[1]
            return self.upbit.get_balance(currency)
        except:
            return 0
    
    def get_current_price(self, ticker):
        return pyupbit.get_current_price(ticker)
"""

files["core/trader.py"] = """import asyncio
import pyupbit
from core.exchange import Exchange
from strategies.base_strategy import Strategy
from core.config import TICKER
from datetime import datetime

class PhoenixTrader:
    def __init__(self):
        self.exchange = Exchange()
        self.strategy = Strategy()
        self.is_running = True
        self.ticker = TICKER
        self.logs = []

    def log(self, msg):
        time = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{time}] {msg}")
        if len(self.logs) > 20: self.logs.pop(0)

    async def run_loop(self):
        self.log("자동매매 엔진 가동")
        while self.is_running:
            try:
                # 데이터 수집 및 전략 실행 시뮬레이션
                price = pyupbit.get_current_price(self.ticker)
                # 실제 매매 로직은 여기에 작성
                await asyncio.sleep(1) 
            except Exception as e:
                # self.log(f"Error: {e}") # 로그 과도하게 쌓임 방지
                await asyncio.sleep(5)

    def get_status(self):
        try:
            price = pyupbit.get_current_price(self.ticker)
            # RSI 계산을 위해 캔들 데이터 가져오기 (예외처리 포함)
            try:
                df = pyupbit.get_ohlcv(self.ticker, interval="minute15", count=50)
                rsi = self.strategy.get_rsi(df)
            except:
                rsi = 0

            return {
                "price": price,
                "rsi": round(rsi, 2) if rsi else 0,
                "logs": self.logs
            }
        except:
            return {"price": 0, "rsi": 0, "logs": self.logs}
"""

# [5] Database & Strategies
files["database/__init__.py"] = ""
files["database/db_manager.py"] = """import sqlite3
class DBManager:
    def __init__(self, db_name="phoenix.db"):
        self.conn = sqlite3.connect(db_name)
"""

files["strategies/__init__.py"] = ""
files["strategies/base_strategy.py"] = """import pandas as pd
class Strategy:
    def get_rsi(self, df, period=14):
        if df is None or len(df) < period: return 0
        delta = df['close'].diff()
        ups = delta.where(delta > 0, 0)
        downs = -delta.where(delta < 0, 0)
        au = ups.rolling(window=period).mean()
        ad = downs.rolling(window=period).mean()
        rsi = au / (au + ad) * 100
        return rsi.iloc[-1]
"""

# [6] Dashboard UI (Tailwind CSS + Dark Mode)
files["templates/dashboard.html"] = """<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phoenix Bot</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #091020; color: white; }
    </style>
</head>
<body class="min-h-screen p-4 flex flex-col items-center">
    <div class="w-full max-w-md space-y-4">
        <div class="flex justify-between items-center border-b border-gray-700 pb-4">
            <h1 class="text-xl font-bold text-yellow-500">🔥 Phoenix Bot</h1>
            <span class="text-xs bg-green-900 text-green-300 px-2 py-1 rounded">RUNNING</span>
        </div>
        
        <div class="bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-700">
            <p class="text-gray-400 text-sm">Bitcoin (KRW)</p>
            <h2 id="price" class="text-4xl font-mono font-bold mt-2">Connecting...</h2>
            <div class="mt-4 flex justify-between items-center bg-gray-900 p-3 rounded-xl">
                <span class="text-sm text-gray-400">RSI (14)</span>
                <span id="rsi" class="font-bold text-blue-400 text-xl">0</span>
            </div>
        </div>

        <div class="bg-black p-4 rounded-xl h-48 overflow-y-auto border border-gray-800 text-xs font-mono space-y-1" id="logs">
            <p class="text-gray-500">System initializing...</p>
        </div>
    </div>

    <script>
        const ws = new WebSocket("ws://" + window.location.host + "/ws");
        ws.onmessage = (e) => {
            const data = JSON.parse(e.data);
            if(data.price) document.getElementById("price").innerText = data.price.toLocaleString() + " KRW";
            if(data.rsi) document.getElementById("rsi").innerText = data.rsi;
            
            const logBox = document.getElementById("logs");
            logBox.innerHTML = "";
            data.logs.slice().reverse().forEach(msg => {
                const p = document.createElement("p");
                p.innerText = msg;
                p.className = "text-green-400";
                logBox.appendChild(p);
            });
        };
    </script>
</body>
</html>
"""

# ==========================================
# 2. 실행
# ==========================================

root_dir = "Project_Phoenix"

if not os.path.exists(root_dir):
    os.makedirs(root_dir)

for path, content in files.items():
    full_path = os.path.join(root_dir, path)
    directory = os.path.dirname(full_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 생성 완료: {full_path}")

print("\n🎉 설치 완료!")
print(f"1. cd {root_dir}")
print("2. pip install -r requirements.txt (이미 했으면 생략)")
print("3. python main.py")
print("4. 브라우저에서 http://127.0.0.1:8000 접속 (지갑 경고 안 뜸)")