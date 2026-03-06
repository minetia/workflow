import random
import time

class IntelligenceTracker:
    """
    제국 정보 모니터링 엔진: 시스템 접속, 외부 유입, AI 동태를 실시간으로 추적 및 기록.
    실제 데이터가 없는 환경에서도 'Magician'의 의도에 맞는 생태계 시뮬레이션 제공.
    """
    def __init__(self):
        self.logs = []
        self.locations = ["Seoul", "New York", "London", "Tokyo", "Dubai", "Singapore", "Marshall Islands"]
        self.access_types = ["VISITOR", "SYSTEM_SEC", "AI_SENTINEL", "EXTERNAL_PING", "ROUTINE_CHECK", "LOGIN_ATTEMPT", "NEWS"]
        self.latest_sentiment = 0.0 # -1.0(악재) ~ 1.0(호재)

    def generate_log(self):
        """가상의 유입 및 접속 데이터 생성: '뉴스' 발생 시 AI 심리에 영향 정보 포함"""
        log_type = random.choice(self.access_types)
        # 평소에는 뉴스 확률을 낮추되, 발생 시 파급력 있게 처리
        if random.random() > 0.8:
            log_type = "NEWS"
            
        location = random.choice(self.locations)
        ip_addr = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        message = ""
        sentiment = 0.0
        
        if log_type == "NEWS":
            news_items = [
                ("Major bank integrates AI for asset management.", 0.8),
                ("New economic policy boosts digital currency adoption.", 0.6),
                ("Global supply chain disruption detected.", -0.7),
                ("Market volatility hits 10-year high.", -0.4),
                ("Tech giant announces proprietary AI trading node.", 0.9),
                ("Regulatory uncertainty causes minor market dip.", -0.5)
            ]
            message, sentiment = random.choice(news_items)
            self.latest_sentiment = sentiment
        elif log_type == "VISITOR":
            message = f"User from {location} viewing the dashboard."
        elif log_type == "SYSTEM_SEC":
            message = f"Encrypted node handshake successful at {location}."
        elif log_type == "AI_SENTINEL":
            message = f"AI Sentinel re-scanning market depth in {location} region."
        elif log_type == "EXTERNAL_PING":
            message = f"Standard ping from aggregator node: {ip_addr}."
        elif log_type == "ROUTINE_CHECK":
            message = f"System health check: All services operational at {location} data center."
        elif log_type == "LOGIN_ATTEMPT":
            message = f"Unauthorized access attempt blocked from {ip_addr}."

        entry = {
            "time": time.strftime("%H:%M:%S"),
            "type": log_type,
            "location": location if log_type != "NEWS" else "GLOBAL",
            "ip": ip_addr,
            "message": message,
            "sentiment": sentiment
        }
        
        self.logs.append(entry)
        if len(self.logs) > 30:
            self.logs.pop(0)
            
        return entry

# Global Tracker Instance
intelligence_tracker = IntelligenceTracker()
