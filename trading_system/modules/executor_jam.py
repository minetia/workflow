"""
# ────────── [ PHOENIX EMPIRE: EXECUTOR JAM ] ────────────
# PHASE 6: THE EXECUTOR - ACTION TERMINAL
# ─────────────────────────────────────────────────────────────
# [MODULE] Executor Jam (The Hand)
# [VERSION] 1.6.0 (EMPIRE)
# ─────────────────────────────────────────────────────────────
"""
import datetime
import logging
# 👑 제국 내부 백엔드 시스템 호출
from backend.matching_engine import matching_engine
from backend.phoenix_vault import phoenix_vault
from backend.bybit_trading_engine import bybit_real_engine

logger = logging.getLogger("PHOENIX.EXECUTOR")

class ExecutorJam:
    """
    PHOENIX V10 - 행동 잼 (The Executor)
    전략을 바탕으로 실제 시장에 주문을 집행합니다.
    """
    def __init__(self, real_trading=False):
        self.name = "Executor_Jam_V10"
        self.is_active = True
        self.real_trading = real_trading # 🚀 사령관 승인 시 True로 변경됨
        self.max_trade_fiat = 100 # 안전을 위해 1회 최대 $100 (KRW 환산 필요 시 조정)

    def execute(self, decision, price, size, risk_score):
        # 1. 리스크 점수가 너무 높으면 실행 차단
        if risk_score > 75:
            return {"status": "FAILED", "reason": "HIGH_RISK_BLOCK"}

        asset = decision.get('asset', 'BTC')
        symbol = f"{asset}USDT"
        action = decision.get('action') # BUY, SELL
        
        # 2. 실전 매매 로직 (Bybit API 연동)
        execution_report = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "asset": asset,
            "executed_price": price,
            "position_size": size,
            "action_taken": action,
            "mode": "REAL" if self.real_trading else "SIMULATION"
        }

        if self.real_trading:
            print(f"🔥 [REAL TRADE] {symbol} {action} {size}개 집행 시도...")
            
            # 🛡️ Safety Check: 1회 미화 100달러 이상 주문 금지
            estimated_fiat = price * size
            if estimated_fiat > self.max_trade_fiat:
                # 수량 강제 조정
                size = self.max_trade_fiat / price
                print(f"⚠️ [SAFETY] 주문 규모가 너무 커서 {size:.4f}개로 자동 축소되었습니다.")

            # Bybit API 호출 (Spot/Linear 구분 필요 - 여기서는 Linear Futures 상정)
            side = "Buy" if action == "BUY" else "Sell"
            resp = bybit_real_engine.place_order(
                category="linear", 
                symbol=symbol, 
                side=side, 
                orderType="Market", 
                qty=size,
                leverage=10 # 기본 레버리지 10배 설정
            )

            if resp.get("retCode") == 0:
                execution_report["execution_status"] = "SUCCESS"
                execution_report["order_id"] = resp["result"].get("orderId")
                print(f"✅ [BYBIT SUCCESS] 주문 번호: {execution_report['order_id']}")
            else:
                execution_report["execution_status"] = "FAILED"
                execution_report["reason"] = resp.get("retMsg", "Unknown Error")
                print(f"❌ [BYBIT FAILED] 사유: {execution_report['reason']}")
        else:
            # 시뮬레이션 모드
            print(f"🚀 [PHOENIX SIM] {asset} {size}개 가상 주문 실행 완료.")
            execution_report["execution_status"] = "SUCCESS"
            execution_report["confidence_score"] = 98

        return execution_report