import os

print("🔥 [Project Phoenix] 시스템 구축을 시작합니다...")

# ==========================================
# 1. 프로젝트 구조 및 파일 내용 정의
# ==========================================

files = {}

# [1] 루트 파일
files["requirements.txt"] = """fastapi
uvicorn
jinja2
python-dotenv
pyupbit
pandas
websockets
"""

files[".env"] = """UPBIT_ACCESS_KEY=your_access_key
UPBIT_SECRET_KEY=your_secret_key
TRADE_TICKER=KRW-BTC
"""

files[".gitignore"] = """.env
__pycache__/
*.db
.DS_Store
"""

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

# 트레이더 인스턴스 생성
trader = PhoenixTrader()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # 1초마다 상태 전송
        data = trader.get_status()
        await websocket.send_json(data)
        await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    # 서버 시작 시 트레이딩 루프 백그라운드 실행
    asyncio.create_task(trader.run_loop())
    print("🚀 Phoenix Trader 백그라운드 실행 시작")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
"""

# [2] Core 모듈
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
        self.upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)

    def get_balance(self, ticker):
        currency = ticker.split('-')[1]
        return self.upbit.get_balance(currency)
    
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
                # 1. 데이터 수집
                df = pyupbit.get_ohlcv(self.ticker, interval="minute15", count=50)
                price = pyupbit.get_current_price(self.ticker)
                
                # 2. 전략 판단
                rsi = self.strategy.get_rsi(df)
                
                # (이곳에 실제 매수/매도 로직이 들어갑니다)
                # 예: if rsi < 30: buy()...

                await asyncio.sleep(1) # 1초 대기
            except Exception as e:
                self.log(f"Error: {e}")
                await asyncio.sleep(5)

    def get_status(self):
        # 웹소켓으로 보낼 데이터
        try:
            price = pyupbit.get_current_price(self.ticker)
            df = pyupbit.get_ohlcv(self.ticker, interval="minute15", count=50)
            rsi = self.strategy.get_rsi(df)
            return {
                "price": price,
                "rsi": round(rsi, 2),
                "logs": self.logs
            }
        except:
            return {"price": 0, "rsi": 0, "logs": self.logs}
"""

# [3] Database 모듈
files["database/__init__.py"] = ""

files["database/db_manager.py"] = """import sqlite3

class DBManager:
    def __init__(self, db_name="phoenix.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                side TEXT,
                price REAL,
                amount REAL
            )
        ''')
        self.conn.commit()
"""

# [4] Strategies 모듈
files["strategies/__init__.py"] = ""

files["strategies/base_strategy.py"] = """import pandas as pd

class Strategy:
    def get_rsi(self, df, period=14):
        delta = df['close'].diff()
        ups = delta.where(delta > 0, 0)
        downs = -delta.where(delta < 0, 0)
        au = ups.rolling(window=period).mean()
        ad = downs.rolling(window=period).mean()
        rsi = au / (au + ad) * 100
        return rsi.iloc[-1]
"""

# [5] Templates (UI)
files["templates/dashboard.html"] = """<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phoenix Bot</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white p-6">
    <div class="max-w-md mx-auto">
        <h1 class="text-2xl font-bold text-yellow-500 mb-4">🔥 Project Phoenix</h1>
        
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg mb-4">
            <p class="text-gray-400 text-sm">현재가 (BTC)</p>
            <h2 id="price" class="text-4xl font-bold">0</h2>
            <div class="mt-4 p-2 bg-gray-700 rounded flex justify-between">
                <span>RSI 지표</span>
                <span id="rsi" class="font-bold text-blue-400">0</span>
            </div>
        </div>

        <div class="bg-black p-4 rounded h-64 overflow-y-auto text-xs font-mono border border-gray-700" id="logs">
            <p class="text-gray-500">시스템 연결 중...</p>
        </div>
    </div>

    <script>
        const ws = new WebSocket("ws://" + window.location.host + "/ws");
        ws.onmessage = (e) => {
            const data = JSON.parse(e.data);
            document.getElementById("price").innerText = data.price.toLocaleString();
            document.getElementById("rsi").innerText = data.rsi;
            
            const logBox = document.getElementById("logs");
            logBox.innerHTML = "";
            data.logs.slice().reverse().forEach(msg => {
                const p = document.createElement("p");
                p.innerText = msg;
                p.className = "mb-1 text-green-400";
                logBox.appendChild(p);
            });
        };
    </script>
</body>
</html>
"""

# ==========================================
# 2. 파일 생성 로직
# ==========================================

root_dir = "Project_Phoenix"

if not os.path.exists(root_dir):
    os.makedirs(root_dir)

for path, content in files.items():
    full_path = os.path.join(root_dir, path)
    
    # 폴더가 있으면 생성
    directory = os.path.dirname(full_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    # 파일 쓰기
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 생성 완료: {full_path}")

print("\n🎉 Project Phoenix 설치가 완료되었습니다!")
print(f"cd {root_dir}")
print("pip install -r requirements.txt")
print("python main.py")