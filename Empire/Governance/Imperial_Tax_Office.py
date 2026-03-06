import sys
import os

# Ensure global dependencies can be resolved
BASE_DIR = r"c:\lovesoong"
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from Empire.Governance.Trading_Ranking_System import trading_ranker

class ImperialTaxOffice:
    """
    제국 세무국: 트레이딩 랭킹에 따른 동적 세금 감면 혜택 계산 및 관리.
    """
    def __init__(self):
        self.base_tax_rate = 0.10 # 기본 10%
        self.rank_benefits = {
            1: 0.02, # 1위: 2% (80% 감면)
            2: 0.05, # 2위: 5% (50% 감면)
            3: 0.08, # 3위: 8% (20% 감면)
            4: 0.10  # 4위: 10% (무감면)
        }

    def get_tax_rate(self, nation_name):
        """성단의 랭킹을 확인하고 적용할 세율 반환"""
        norm_name = nation_name.replace("CASTLE_", "").capitalize()
        
        # 🏆 [Grand Prix Champion Check]
        try:
            from Empire.Governance.Imperial_Trading_Grand_Prix import imperial_grand_prix
            elites = imperial_grand_prix.get_hall_of_fame()
            current_cycle = datetime.now().strftime("%Y-%m")
            if current_cycle in elites and elites[current_cycle]["origin"] == norm_name:
                print(f"🎖️ [Champion Benefit] {norm_name} is the ITGP Champion! Applying 0.5% special rate.")
                return 0.005, 1, 95.0 # 95% reduction
        except: pass

        rank = trading_ranker.get_rank(norm_name)
        rate = self.rank_benefits.get(rank, self.base_tax_rate)
        
        reduction = (self.base_tax_rate - rate) / self.base_tax_rate * 100
        return rate, rank, reduction

    def calculate_tax(self, nation_name, amount):
        rate, rank, reduction = self.get_tax_rate(nation_name)
        tax_amount = amount * rate
        return tax_amount, rate, rank, reduction

# Global Instance
imperial_tax_office = ImperialTaxOffice()
