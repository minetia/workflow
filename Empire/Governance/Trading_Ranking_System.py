import random
import time

class TradingRankingSystem:
    """
    제국 트레이딩 랭킹 시스템: 4개 성단(Alpha, Core, Nexus, Zion)의 실적을 바탕으로 매시간 순위를 산정.
    """
    def __init__(self):
        self.nations = ["Alpha", "Core", "Nexus", "Zion"]
        self.current_rankings = {}
        self.initialize_rankings()

    def initialize_rankings(self):
        """초기 랭킹 수작업 설정 (또는 랜덤 초기화)"""
        random.shuffle(self.nations)
        self.current_rankings = {nation: i+1 for i, nation in enumerate(self.nations)}

    def update_rankings(self):
        """실제 트레이딩 성과(시뮬레이션)를 바탕으로 랭킹 갱신"""
        # 각 성단의 성과 점수 산출
        performance = {nation: random.uniform(50, 100) for nation in self.nations}
        # 점수 기준 내림차순 정렬
        sorted_nations = sorted(performance.items(), key=lambda x: x[1], reverse=True)
        
        self.current_rankings = {nation: i+1 for i, (nation, score) in enumerate(sorted_nations)}
        
        print(f"📊 [Governance] 실시간 트레이딩 랭킹 갱신 완료:")
        for nation, rank in self.current_rankings.items():
            print(f"  > Rank {rank}: {nation} 성단 (Score: {performance[nation]:.2f})")
        
        return self.current_rankings

    def get_rank(self, nation):
        return self.current_rankings.get(nation, 4)

# Global Instance
trading_ranker = TradingRankingSystem()
