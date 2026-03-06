import time
from datetime import datetime, timedelta
from typing import Dict, Optional

class AILoanVault:
    """
    제국 AI 대출 및 형벌 관리소.
    AI 요원들에게 시드머니를 대출해주고, 파산 시 회차 관리 및 강제 노역을 집행함.
    """
    def __init__(self):
        self.SEED_AMOUNT = 10_000_000  # 1,000만 원
        self.MAX_LOANS = 3
        self.LABOR_DURATION_HOURS = 12  # 강제 노역 시간
        
        # AI 상태 저장소: {ai_id: {loan_count, balance, status, labor_end_time}}
        self.ai_states: Dict[str, dict] = {}

    def initialize_ai(self, ai_id: str):
        """신규 AI 요원에게 최초 대출 집행"""
        if ai_id not in self.ai_states:
            self.ai_states[ai_id] = {
                "loan_count": 1,
                "balance": self.SEED_AMOUNT,
                "status": "TRADING",
                "labor_end_time": None,
                "total_bankruptcy": 0
            }
        return self.ai_states[ai_id]

    def process_bankruptcy(self, ai_id: str) -> dict:
        """AI 파산 처리 및 대출/노역 판정"""
        state = self.ai_states.get(ai_id)
        if not state:
            return {"error": "AI_NOT_FOUND"}

        state["total_bankruptcy"] += 1
        
        if state["loan_count"] < self.MAX_LOANS:
            # 주군의 자비: 추가 대출
            state["loan_count"] += 1
            state["balance"] = self.SEED_AMOUNT
            state["status"] = f"TRADING (Loan {state['loan_count']})"
        else:
            # 자비 끝: 강제 노역 투입
            state["status"] = "FORCED_LABOR"
            state["labor_end_time"] = (datetime.now() + timedelta(hours=self.LABOR_DURATION_HOURS)).strftime("%Y-%m-%d %H:%M:%S")
            state["balance"] = 0
            
        return state

    def check_labor_release(self, ai_id: str):
        """노역 시간 종료 여부 확인 및 석방"""
        state = self.ai_states.get(ai_id)
        if state and state["status"] == "FORCED_LABOR":
            end_time = datetime.strptime(state["labor_end_time"], "%Y-%m-%d %H:%M:%S")
            if datetime.now() >= end_time:
                # 노역형 종료 -> 다시 1회차 대출로 갱생 기회 부여
                state["status"] = "TRADING (Released)"
                state["loan_count"] = 1
                state["balance"] = self.SEED_AMOUNT
                state["labor_end_time"] = None
                return True
        return False

    def get_ai_status(self, ai_id: str):
        return self.ai_states.get(ai_id, {"status": "NOT_ENLISTED"})

ai_loan_vault = AILoanVault()
