import os
import json
from datetime import datetime

class AITradingPermit:
    """
    네트워크부 5분과: AI 트레이딩 허가 및 세금 관리 엔진
    - 허가제 도입: 제국의 허가를 받은 사용자만 참여 가능
    - 세금 시스템: 총 수익금의 10% 징수 (피닉스 5%, 현실 5%)
    """
    def __init__(self):
        self.base_path = r'C:\Users\loves\workflow\data'
        self.permit_file = os.path.join(self.base_path, 'trading_permits.json')
        self.tax_log_file = os.path.join(self.base_path, 'trading_tax_logs.json')
        self._ensure_files()

    def _ensure_files(self):
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        for f in [self.permit_file, self.tax_log_file]:
            if not os.path.exists(f):
                with open(f, 'w', encoding='utf-8') as file:
                    json.dump([], file)

    def issue_permit(self, user_id, reason="Imperial Grade Approval"):
        """거래 허가증 발급"""
        permits = self.get_all_permits()
        if any(p['user_id'] == user_id for p in permits):
            return {"success": False, "message": "이미 허가된 사용자입니다."}
            
        new_permit = {
            "user_id": user_id,
            "status": "APPROVED",
            "issued_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reason": reason
        }
        permits.append(new_permit)
        with open(self.permit_file, 'w', encoding='utf-8') as f:
            json.dump(permits, f, indent=4)
        return {"success": True, "message": f"[{user_id}] 사령관님의 성은으로 거래 허가가 승인되었습니다."}

    def check_permit(self, user_id):
        permits = self.get_all_permits()
        return any(p['user_id'] == user_id and p['status'] == "APPROVED" for p in permits)

    def get_all_permits(self):
        try:
            with open(self.permit_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []

    def settle_profit(self, user_id, profit_amount):
        """수익 정산 및 10% 세금 징수 (5:5 배분)"""
        if not self.check_permit(user_id):
            return {"success": False, "message": "허가되지 않은 사용자의 수익 정산 시도입니다."}

        tax_total = profit_amount * 0.10
        tax_phoenix = tax_total * 0.5  # 5%
        tax_real = tax_total * 0.5     # 5%
        net_profit = profit_amount - tax_total

        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": user_id,
            "gross_profit": profit_amount,
            "tax_total": tax_total,
            "tax_phoenix_vault": tax_phoenix,
            "tax_real_vault": tax_real,
            "net_profit": net_profit
        }

        logs = self.get_tax_logs()
        logs.append(log_entry)
        with open(self.tax_log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=4)

        return {
            "success": True,
            "net_profit": net_profit,
            "tax_paid": tax_total,
            "distribution": {"phoenix": tax_phoenix, "real": tax_real}
        }

    def get_tax_logs(self):
        try:
            with open(self.tax_log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []

trading_permit_engine = AITradingPermit()
