import pyupbit
import pandas as pd
import time
import logging
from datetime import datetime

class AutoTrader:
    def __init__(self, access_key, secret_key, ticker, invest_ratio):
        self.upbit = pyupbit.Upbit(access_key, secret_key)
        self.ticker = ticker
        self.invest_ratio = float(invest_ratio)
        self.is_running = False
        self.status_log = []
        
        # 로깅 설정
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("PhoenixTrader")

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        self.logger.info(log_msg)
        self.status_log.append(log_msg)
        if len(self.status_log) > 50: self.status_log.pop(0)

    def get_balance(self):
        """현금 및 코인 잔고 조회"""
        try:
            krw = self.upbit.get_balance("KRW")
            coin = self.upbit.get_balance(self.ticker)
            return krw, coin
        except Exception as e:
            self.log(f"Error getting balance: {e}")
            return 0, 0

    def get_market_status(self):
        """RSI 및 이동평균선 분석 (전략 엔진)"""
        df = pyupbit.get_ohlcv(self.ticker, interval="minute15", count=100)
        
        # RSI 계산
        delta = df['close'].diff()
        ups = delta.where(delta > 0, 0)
        downs = -delta.where(delta < 0, 0)
        au = ups.rolling(window=14).mean()
        ad = downs.rolling(window=14).mean()
        rsi = au / (au + ad) * 100
        
        current_rsi = rsi.iloc[-1]
        current_price = df['close'].iloc[-1]
        
        return current_price, current_rsi

    def execute_strategy(self, rsi_buy, rsi_sell, stop_loss, target_profit):
        if not self.is_running:
            return "Stopped"

        try:
            krw_balance, coin_balance = self.get_balance()
            current_price, rsi = self.get_market_status()
            avg_buy_price = self.upbit.get_avg_buy_price(self.ticker)

            self.log(f"Price: {current_price} | RSI: {rsi:.2f} | MyCoin: {coin_balance}")

            # 1. 매수 로직 (RSI 과매도 구간)
            if rsi < rsi_buy and krw_balance > 5000:
                buy_amount = krw_balance * self.invest_ratio
                self.upbit.buy_market_order(self.ticker, buy_amount)
                self.log(f"🔥 매수 체결! (RSI: {rsi:.2f})")

            # 2. 매도 로직 (보유 중일 때만)
            if coin_balance > 0.00001:
                profit_rate = (current_price - avg_buy_price) / avg_buy_price
                
                # 익절 (RSI 과매수 or 목표 수익)
                if rsi > rsi_sell or profit_rate >= target_profit:
                    self.upbit.sell_market_order(self.ticker, coin_balance)
                    self.log(f"💰 익절 성공! 수익률: {profit_rate*100:.2f}%")
                
                # 손절 (방어 로직)
                elif profit_rate <= -stop_loss:
                    self.upbit.sell_market_order(self.ticker, coin_balance)
                    self.log(f"🛡️ 손절 방어 동작. 손실률: {profit_rate*100:.2f}%")

        except Exception as e:
            self.log(f"Trading Error: {e}")

        return "Active"