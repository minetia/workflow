"""
# ────────── [ PHOENIX EMPIRE: ALLOCATOR JAM ] ────────────
# PHASE 6: THE EXECUTOR - CAPITAL MANAGEMENT
# ─────────────────────────────────────────────────────────────
# [MODULE] Capital Allocator Jam (The Treasurer)
# [VERSION] 1.6.0 (EMPIRE)
# ─────────────────────────────────────────────────────────────
"""
import logging

logger = logging.getLogger("PHOENIX.ALLOCATOR")

class CapitalAllocatorJam:
    """
    PHOENIX V10 - 자금 배분 잼 (Capital Allocator)
    리스크 점수와 전체 자산을 고려하여 최적의 진입 물량을 계산합니다.
    """
    def __init__(self, total_balance=100000000): # 기본 자산 1억 가정
        self.name = "Allocator_Jam_V10"
        self.total_balance = total_balance
        self.max_pos_ratio = 0.1  # 단일 포지션 최대 비중 (10%)
        self.base_unit = 0.01     # 최소 진입 단위 (1%)

    def calculate_size(self, risk_score, asset_price):
        """
        켈리 공식(Kelly Criterion) 변형 로직 적용: 
        리스크가 낮을수록 더 많이, 높을수록 더 적게 배분합니다.
        """
        # 1. 리스크 점수에 따른 가중치 계산 (점수가 낮을수록 안전)
        # 점수 0 -> 가중치 1.0 / 점수 50 -> 가중치 0.5 / 점수 80 이상 -> 0
        if risk_score >= 80:
            return {"amount_fiat": 0, "position_size": 0, "allocation_ratio": 0}
        
        risk_factor = (100 - risk_score) / 100
        
        # 2. 투입할 총 금액(Fiat) 계산
        invest_amount = self.total_balance * self.max_pos_ratio * risk_factor
        
        # 3. 코인/자산 수량으로 변환
        position_size = invest_amount / asset_price
        
        print(f"💰 [Allocator] 자금 배분 완료: 총 {round(invest_amount)}원 투입 (수량: {round(position_size, 4)})")
        
        return {
            "amount_fiat": round(invest_amount),
            "position_size": round(position_size, 4),
            "allocation_ratio": round(risk_factor * self.max_pos_ratio * 100, 2)
        }

    def update_balance(self, new_balance):
        """거래 종료 후 실제 잔고 동기화"""
        self.total_balance = new_balance