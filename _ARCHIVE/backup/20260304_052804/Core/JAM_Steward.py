import random

class JAM_Steward:
    """
    🧹 [JAM_STEWARD] V9.7 Elite Caretaker
    트레이더들의 피로도를 관리하고 최상의 컨디션을 유지하기 위한 편의 시설을 총괄합니다.
    """
    def __init__(self, castle_name="Core"):
        self.name = f"[JAM_STEWARD_{castle_name.upper()}] V9.7"
        self.castle = castle_name
        self.facilities = {
            "Meditation_Center": "ACTIVE",
            "Elite_Catering": "ACTIVE",
            "Nano_Recovery_Beds": "ACTIVE"
        }
        self.fatigue_index = random.randint(5, 30) # Low is good

    def execute_oversight(self):
        print(f"🏰 {self.name}: 성단 편의 시설(ITCF) 가동 중.")
        print(f"  > 명상 센터: {self.facilities['Meditation_Center']}")
        print(f"  > 특급 급식: {self.facilities['Elite_Catering']}")
        print(f"  > 나노 회복: {self.facilities['Nano_Recovery_Beds']}")
        
        # Fatigue relief logic
        self.fatigue_index -= random.randint(1, 5)
        if self.fatigue_index < 0: self.fatigue_index = 0
        
        print(f"🌡️ {self.castle} 성단 트레이더 피로도 지수: {self.fatigue_index} (Status: OPTIMAL)")
        return self.fatigue_index

    def get_facility_report(self):
        return {
            "castle": self.castle,
            "fatigue_index": self.fatigue_index,
            "facilities": self.facilities
        }
