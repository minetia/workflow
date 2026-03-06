import time
import random
import json
import os

# 가상의 고래 지갑 주소 목록
WHALE_WALLETS = [
    "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
    "0x71C7656EC7ab88b098defB751B7401B5f6d8976F",
    "0xb8c77482e45F1F44dE1745F52C74426C631bDD52"
]

def start_collection():
    print("====================================")
    print(" [DATA_VAULT] 고래 지갑 수집 모튤 가동 ")
    print("====================================")
    
    while True:
        try:
            # 3~7초 단위로 수집 시뮬레이션
            time.sleep(random.uniform(3, 7))
            
            wallet = random.choice(WHALE_WALLETS)
            amount = round(random.uniform(50, 1000), 2)
            coin = random.choice(["BTC", "ETH", "SOL"])
            action = random.choice(["BUY", "SELL", "TRANSFER"])
            
            log_msg = f"[WHALE ALERT] {wallet[:6]}...{wallet[-4:]} | {action} {amount} {coin}"
            print(log_msg)
            
            # 실시간 로그 기록용 파일 생성 (선택 사항)
            log_dir = os.path.dirname(__file__)
            log_path = os.path.join(log_dir, "whale_log.txt")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {log_msg}\n")
                
        except KeyboardInterrupt:
            print("\n[DATA_VAULT] 수집 모듈 정지.")
            break

if __name__ == "__main__":
    start_collection()
