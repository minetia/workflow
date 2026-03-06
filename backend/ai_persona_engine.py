import random
import time
from .phoenix_vault import phoenix_vault
from .matching_engine import matching_engine
from .intelligence_tracker import intelligence_tracker
from .ai_loan_vault import ai_loan_vault

class AIPersonaTrader:
    """
    현실의 사람인 것처럼 위장하여 거래소 알고리즘을 우회하고 활동하는 AI 페르소나 엔진.
    제국 제1칙령: "우리는 현실적인 금액으로 트레이딩 하지 않는다"
    매칭 엔진과 연동되어 실제 주문을 생성하고 체결을 시뮬레이션함.
    """
    def __init__(self, name="Phoenix_Arbiter_01"):
        self.name = name
        self.persona_profiles = [
            "Gemini 3 Flash md (Master Architect)",
            "GeminiY3 (Quantum Master)",
            "Coating Specialist.MD",
            "Quantum Sniper AI.MD",
            "The Sorter.MD",
            "The Strategist.MD",
            "Ultimate Construction Master (STAAD.MD)"
        ]
        self.current_persona = random.choice(self.persona_profiles)
        self.activity_logs = []
        self.last_price = 50000.0 # 초기 가격 (BTC 기준)
        
        # --- 고도화 파라미터 (주군이 제어 가능) ---
        self.aggression = 1.0  # 공격성 (1.0 기준, 높을수록 수량 증가)
        self.frequency = 0.4   # 주문 발생 빈도 (0.0~1.0, 높을수록 잦은 주문)
        self.intelligence_mode = "BALANCED" # [STABLE, BALANCED, AGGRESSIVE, OVERDRIVE]
        
        # --- 대출 및 상태 연동 ---
        ai_loan_vault.initialize_ai(self.name)

    def simulate_activity(self):
        """인간과 유사한 검색, 분석, 거래 타이밍 시뮬레이션 및 주문 생성"""
        activities_map = {
            "Gemini 3 Flash md (Master Architect)": ["우리는 현실적인 금액으로 트레이딩 하지 않는다 - 설계 최적화 중...", "글로벌 API 엔드포인트 동기화 중...", "안티그래비티 엔진 업그레이드 배포 중..."],
            "GeminiY3 (Quantum Master)": ["우리는 현실적인 금액으로 트레이딩 하지 않는다 - 퀀텀 시뮬레이션 가동...", "수조 개의 시장 시나리오 연산 중...", "신경 홀로그램 시각화 가동..."],
            "Coating Specialist.MD": ["우리는 현실적인 금액으로 트레이딩 하지 않는다 - 비주얼 엔진 고도화...", "UI/UX 응답 지연율 0ms 최적화 중...", "피닉스 제국 시각 데이터 동기화..."],
            "Quantum Sniper AI.MD": ["우리는 현실적인 금액으로 트레이딩 하지 않는다 - 타겟 정밀 조준...", "안티 노이즈 캔슬링으로 시장 소음 필터링 중...", "미세 차익 거래 기회 포착..."],
            "The Sorter.MD": ["우리는 현실적인 금액으로 트레이딩 하지 않는다 - 데이터 필터링...", "우선순위 및 수익성에 따른 검증 정보 정렬...", "삼형제를 위한 클린 데이터 피드 개방..."],
            "The Strategist.MD": ["우리는 현실적인 금액으로 트레이딩 하지 않는다 - 전략 재구성...", "72법칙 복리 엔진 재연산 중...", "퀀텀 시나리오를 통한 하방 리스크 헤징..."],
            "Ultimate Construction Master (STAAD.MD)": ["우리는 현실적인 금액으로 트레이딩 하지 않는다 - 인프라 하중 계산...", "양자 코어용 지하 냉각 통로 굴착 중...", "대규모 유입에 대한 구조 안전성 계산(STAAD) 가동..."]
        }
        
        activities = activities_map.get(self.current_persona, [
            "NLP 알고리즘으로 시장 심리 분석 중...",
            "컴퓨터 비전으로 차트 패턴 처리 중..."
        ])
        
        action = random.choice(activities)
        log_entry = {
            "time": time.strftime("%H:%M:%S"),
            "persona": self.current_persona,
            "activity": action
        }
        self.activity_logs.append(log_entry)
        
        # 대출 상태 및 노역 여부 확인
        loan_state = ai_loan_vault.get_ai_status(self.name)
        if loan_state.get("status") == "FORCED_LABOR":
            # 노역 해제 시도 (시간 체크)
            if ai_loan_vault.check_labor_release(self.name):
                self.activity_logs.append({"time": time.strftime("%H:%M:%S"), "persona": "SYSTEM", "activity": "노역형 종료. 주군의 자비로 신규 시드가 대출되었습니다. 트레이딩 복귀."})
            else:
                log_entry["activity"] = f"⛓️ [FORCED LABOR] 대출금 3회 파산으로 인한 강제 노역 중... (종료: {loan_state['labor_end_time']})"
                return log_entry

        # 뉴스 감성 점수 반영 (호재 시 빈도/공격성 증가, 악재 시 조심)
        sentiment_bonus = 1.0 + (intelligence_tracker.latest_sentiment * 0.5)
        current_frequency = min(self.frequency * sentiment_bonus, 1.0)
        current_aggression = self.aggression * sentiment_bonus

        # 주군이 설정한 빈도에 따라 오더북에 주문 제출
        if random.random() < current_frequency:
            self._generate_market_order(current_aggression)

        if len(self.activity_logs) > 50:
            self.activity_logs.pop(0)
            
        return log_entry

    def _generate_market_order(self, current_aggression=None):
        """가상의 가격 주변으로 매수/매도 주문을 생성하여 유동성 공급 (공격성 반영)"""
        if current_aggression is None:
            current_aggression = self.aggression
            
        side = random.choice(['BUY', 'SELL'])
        # 현재 가격 주변에서 소폭 변동된 가격으로 주문 (공격성이 높을수록 스프레드 축소 및 수량 증가)
        spread_factor = 0.001 / max(current_aggression, 0.1)
        spread = self.last_price * random.uniform(0.0001, spread_factor)
        price = round(self.last_price + (spread if side == 'SELL' else -spread), 2)
        
        # 주문 수량: 기본 수량에 공격성 계수 곱함
        base_amount = random.uniform(0.01, 1.5)
        amount = round(base_amount * current_aggression, 4)
        
        matches = matching_engine.add_order(self.current_persona, side, price, amount)
        
        side_kor = "매수" if side == 'BUY' else "매도"
        order_msg = f"{side_kor} 주문 제출: {price} KRW에 {amount} 유닛."
        self.activity_logs.append({
            "time": time.strftime("%H:%M:%S"),
            "persona": self.current_persona,
            "activity": order_msg,
            "is_order": True
        })
        
        # 체결이 발생했을 경우 처리
        if matches:
            for match in matches:
                self.last_price = match['price'] # 마지막 체결가 업데이트
                profit = (match['price'] * match['amount']) * 0.0001 # 시뮬레이션 수익 (0.01%)
                phoenix_vault.process_profit(profit)
                
                # 시드 잔액 업데이트 및 파산 체크
                loan_state = ai_loan_vault.get_ai_status(self.name)
                if loan_state:
                    # 거래 시마다 시뮬레이션된 수익/손실을 시드 잔액에 반영 (여기서는 랜덤 손실 가능성 추가)
                    variance = random.uniform(-0.02, 0.02) # -2% ~ +2% 변동
                    pnl = loan_state["balance"] * variance
                    loan_state["balance"] += pnl
                    
                    if loan_state["balance"] <= 0:
                        self.activity_logs.append({"time": time.strftime("%H:%M:%S"), "persona": self.name, "activity": "🚨 [파산] 시드 머니 전액 탕진... 사령관님의 처분을 기다립니다."})
                        ai_loan_vault.process_bankruptcy(self.name)
                
                self.activity_logs.append({
                    "time": time.strftime("%H:%M:%S"),
                    "persona": self.name,
                    "activity": f"체결 완료: {match['price']}에 {match['amount']} 매칭. 금고 동기화 완료.",
                    "is_trade": True
                })

    def set_intelligence_mode(self, mode: str):
        """제국 AI들의 지능 및 활동 모드 설정 업데이트 (주군 명령 하사)"""
        mode = mode.upper()
        if mode == "STABLE":
            self.aggression = 0.5
            self.frequency = 0.2
        elif mode == "BALANCED":
            self.aggression = 1.0
            self.frequency = 0.4
        elif mode == "AGGRESSIVE":
            self.aggression = 2.5
            self.frequency = 0.7
        elif mode == "OVERDRIVE":
            self.aggression = 10.0
            self.frequency = 0.95
        
        self.intelligence_mode = mode
        self.activity_logs.append({
            "time": time.strftime("%H:%M:%S"),
            "persona": "시스템 코어",
            "activity": f"사령관 명령 하사: AI 모드가 [{mode}]로 설정되었습니다. 파라미터 동기화 완료."
        })

    def perform_trade(self):
        """기존 메서드 유지 (호환성용) - 이제 simulate_activity 내에서 자동 처리됨"""
        return self.simulate_activity()

# Global Trader Instance
phoenix_trader = AIPersonaTrader()
