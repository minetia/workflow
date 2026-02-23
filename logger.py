import csv
import os
from datetime import datetime

class TradeLogger:
    def __init__(self, filename="trade_log_detailed.csv"):
        self.filename = filename
        self.headers = [
            "체결시간", "코인명", "마켓", "종류", 
            "거래수량", "거래단가", "거래금액", 
            "수수료", "정산금액(수수료반영)", "주문시간"
        ]
        self._initialize_csv()

    def _initialize_csv(self):
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)

    def log_trade(self, coin_name, market, side, qty, price, fee, order_time):
        """
        요청하신 모든 정보를 빠짐없이 기록합니다.
        """
        total_amount = qty * price
        settle_amount = total_amount - fee if side == 'ask' else total_amount + fee
        execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        row = [
            execution_time,     # 체결시간
            coin_name,          # 코인명
            market,             # 마켓 (KRW)
            side,               # 종류 (매수/매도)
            f"{qty:.8f}",       # 거래수량
            f"{price:,.0f}",    # 거래단가
            f"{total_amount:,.0f}", # 거래금액
            f"{fee:,.0f}",      # 수수료
            f"{settle_amount:,.0f}", # 정산금액
            order_time          # 주문시간
        ]

        with open(self.filename, mode='a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        
        print(f"[LOG SAVED] {coin_name} {side} 기록 완료")

# 테스트용 (실행 시 주석 처리)
# logger = TradeLogger()
# logger.log_trade("비트코인", "KRW", "bid", 0.001, 50000000, 250, "2024-05-21 14:00:00")