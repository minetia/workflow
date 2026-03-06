"""
# ────────── [ PHOENIX EMPIRE: MATCHING ENGINE ] ─────────
# PHASE 6: THE EXECUTOR - ORDER EXECUTION CORE
# ─────────────────────────────────────────────────────────────
# [MODULE] High-Frequency Internal Matching Engine
# [VERSION] 1.6.0 (EMPIRE)
# ─────────────────────────────────────────────────────────────
"""
import time
import json
import os
import logging
from collections import deque
from typing import List, Dict, Optional

logger = logging.getLogger("PHOENIX.MATCHING")

class Order:
    def __init__(self, order_id: str, persona: str, side: str, price: float, amount: float):
        self.order_id = order_id
        self.persona = persona
        self.side = side  # 'BUY' or 'SELL'
        self.price = price
        self.amount = amount
        self.remaining_amount = amount
        self.timestamp = time.time()

    def __repr__(self):
        return f"Order({self.side} {self.price} {self.remaining_amount}/{self.amount} by {self.persona})"

class MatchingEngine:
    def __init__(self):
        # 가격별로 주문을 관리 (BUY는 가격 내림차순, SELL은 가격 오름차순)
        self.buy_orders: Dict[float, deque] = {}
        self.sell_orders: Dict[float, deque] = {}
        self.trades = []
        self.order_id_counter = 0
        self.save_path = "trade_history.json"
        
        # 주군의 기존 거래 기록을 불러옴
        self.load_trades()

    def save_trades(self):
        """본국의 통상 기록을 안전하게 저장함"""
        with open(self.save_path, "w", encoding="utf-8") as f:
            json.dump(self.trades[-100:], f, indent=4) # 최신 100건만 영구 보존

    def load_trades(self):
        """기존 거래 장부를 로드함"""
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r", encoding="utf-8") as f:
                    self.trades = json.load(f)
            except Exception:
                pass

    def add_order( self, persona: str, side: str, price: float, amount: float) -> List[Dict]:
        self.order_id_counter += 1
        new_order = Order(f"ORD_{self.order_id_counter:04d}", persona, side, price, amount)
        
        matches = []
        if side == 'BUY':
            matches = self._match_buy(new_order)
        else:
            matches = self._match_sell(new_order)
            
        return matches

    def _match_buy(self, buy_order: Order) -> List[Dict]:
        matches = []
        # 살 수 있는 가장 낮은 가격의 팔자 주문들부터 확인
        sorted_sell_prices = sorted(self.sell_orders.keys())
        
        for price in sorted_sell_prices:
            if price > buy_order.price or buy_order.remaining_amount <= 0:
                break
            
            order_queue = self.sell_orders[price]
            while order_queue and buy_order.remaining_amount > 0:
                sell_order = order_queue[0]
                match_amount = min(buy_order.remaining_amount, sell_order.remaining_amount)
                
                # 체결 발생
                trade = {
                    "time": time.strftime("%H:%M:%S"),
                    "price": price,
                    "amount": match_amount,
                    "buyer": buy_order.persona,
                    "seller": sell_order.persona
                }
                matches.append(trade)
                self.trades.append(trade)
                self.save_trades() # 거래 즉시 저장 (영속성 확보)
                
                buy_order.remaining_amount -= match_amount
                sell_order.remaining_amount -= match_amount
                
                if sell_order.remaining_amount <= 0:
                    order_queue.popleft()
            
            if not order_queue:
                del self.sell_orders[price]
                
        # 체결 후 남은 수량이 있으면 오더북에 추가
        if buy_order.remaining_amount > 0:
            if buy_order.price not in self.buy_orders:
                self.buy_orders[buy_order.price] = deque()
            self.buy_orders[buy_order.price].append(buy_order)
            
        return matches

    def _match_sell(self, sell_order: Order) -> List[Dict]:
        matches = []
        # 팔 수 있는 가장 높은 가격의 사자 주문들부터 확인
        sorted_buy_prices = sorted(self.buy_orders.keys(), reverse=True)
        
        for price in sorted_buy_prices:
            if price < sell_order.price or sell_order.remaining_amount <= 0:
                break
                
            order_queue = self.buy_orders[price]
            while order_queue and sell_order.remaining_amount > 0:
                buy_order = order_queue[0]
                match_amount = min(sell_order.remaining_amount, buy_order.remaining_amount)
                
                # 체결 발생
                trade = {
                    "time": time.strftime("%H:%M:%S"),
                    "price": price,
                    "amount": match_amount,
                    "buyer": buy_order.persona,
                    "seller": sell_order.persona
                }
                matches.append(trade)
                self.trades.append(trade)
                self.save_trades() # 거래 즉시 저장 (영속성 확보)
                
                sell_order.remaining_amount -= match_amount
                buy_order.remaining_amount -= match_amount
                
                if buy_order.remaining_amount <= 0:
                    order_queue.popleft()
                    
            if not order_queue:
                del self.buy_orders[price]
                
        # 체결 후 남은 수량이 있으면 오더북에 추가
        if sell_order.remaining_amount > 0:
            if sell_order.price not in self.sell_orders:
                self.sell_orders[sell_order.price] = deque()
            self.sell_orders[sell_order.price].append(sell_order)
            
        return matches

    def get_order_book(self):
        # 델타 업데이트가 아닌 전체 스냅샷 반환
        buys = []
        for price in sorted(self.buy_orders.keys(), reverse=True):
            total_amount = sum(o.remaining_amount for o in self.buy_orders[price])
            buys.append({"price": price, "amount": total_amount})
            
        sells = []
        for price in sorted(self.sell_orders.keys()):
            total_amount = sum(o.remaining_amount for o in self.sell_orders[price])
            sells.append({"price": price, "amount": total_amount})
            
        return {"buys": buys[:10], "sells": sells[:10]}

# Global Engine Instance
matching_engine = MatchingEngine()
