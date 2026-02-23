import pyupbit
from core.config import ACCESS_KEY, SECRET_KEY

class Exchange:
    def __init__(self):
        self.upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)

    def get_balance(self, ticker):
        currency = ticker.split('-')[1]
        return self.upbit.get_balance(currency)
    
    def get_current_price(self, ticker):
        return pyupbit.get_current_price(ticker)
