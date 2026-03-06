import random
import time
from datetime import datetime

class TradingInfoCenter:
    """
    제국 정보관: 50개 지표 및 30개 뉴스 피드 총괄
    """
    def __init__(self):
        self.indicators = self._generate_base_indicators(55)
        self.news_sources = [
            "Bloomberg Terminal", "Reuters Alpha", "WSJ Market Catch", "FT Global", "Nikkei Asia",
            "CNBC Live", "Yahoo Finance Premium", "Investing.com Pro", "MarketWatch", "Forbes Market",
            "Financial Times Intelligence", "ZeroHedge", "Kitco Metals", "CoinTelegraph", "CoinDesk",
            "Blockworks", "The Block", "Glassnode", "Santiment", "Messari",
            "CryptoQuant", "TradingView News", "Benzinga", "Seeking Alpha", "Fool.com",
            "Business Insider", "Economist Intelligence", "IMF Data Feed", "FED Monitor", "ECB Watch"
        ]
        self.news_feed = []
        self._usage_fee_per_info = 15.5 # PQC
        
    def _generate_base_indicators(self, count):
        inds = []
        prefixes = ["QUANTUM", "SOLAR", "MARS", "NEURAL", "PHOENIX", "MASTER", "VOID", "ETHER"]
        suffixes = ["INDEX", "POWER", "RATIO", "VOL", "FLOW", "DELTA", "ALPHA", "OMEGA"]
        for i in range(count):
            name = f"{random.choice(prefixes)}_{random.choice(suffixes)}_{i+1:02d}"
            inds.append({"name": name, "value": random.uniform(10, 5000), "change": 0.0})
        return inds

    def get_realtime_indicators(self):
        for ind in self.indicators:
            delta = random.uniform(-10, 10)
            ind["value"] += delta
            ind["change"] = delta
        return self.indicators

    def get_realtime_news(self):
        source = random.choice(self.news_sources)
        subjects = ["Quantum Volatility Spikes", "Empire Asset Surge", "AI Profit Optimization", "Market Fusion Detected", "Central Bank Digital Shift"]
        news = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "source": source,
            "headline": f"[{source}] {random.choice(subjects)} - Breaking Report"
        }
        self.news_feed.insert(0, news)
        self.news_feed = self.news_feed[:30] # 최근 30개 유지
        return self.news_feed

    def charge_usage_fee(self, user_id):
        # 정보 이용료 부과 (시뮬레이션 로그)
        return {
            "success": True, 
            "fee": self._usage_fee_per_info,
            "message": f"제국 정보 이용료 {self._usage_fee_per_info} PQC가 부과되었습니다. 고차원 데이터 접근이 허용됩니다."
        }

trading_info_center = TradingInfoCenter()
