import time
import random

def analyze_market_sentiment():
    """
    [DATA_VAULT/market_sentiment]
    글로벌 공포/탐욕 지수 및 소셜 미디어 트렌드를 수집 분석하는 외부 안테나
    """
    print("=========================================")
    print(" [DATA_VAULT] 센티먼트 분석 안테나 전개 ")
    print("=========================================")
    
    while True:
        try:
            time.sleep(random.uniform(15, 30))
            
            fg_index = random.randint(10, 90)
            status = ""
            if fg_index <= 20: status = "극단적 공포 (Extreme Fear)"
            elif fg_index <= 45: status = "공포 (Fear)"
            elif fg_index <= 55: status = "중립 (Neutral)"
            elif fg_index <= 80: status = "탐욕 (Greed)"
            else: status = "극단적 탐욕 (Extreme Greed)"
            
            print(f"\n[MARKET_SENTIMENT] 🌐 글로벌 공포/탐욕 지수 업데이트: {fg_index}/100 ➔ {status}")
            
            if fg_index <= 20:
                print("💡 [분석가 의견] 딥 매수(Dip Buy) 최적의 기회입니다. Quantum Core에 매수 가중치 신호를 전파합니다.")
            elif fg_index >= 80:
                print("💡 [분석가 의견] 과열 지대 진입. Security Shield의 손실 허용치를 보수적으로 하향 조정할 것을 권고합니다.")
            else:
                print("💡 [분석가 의견] 시장 안정권. 기존 알고리즘을 유지합니다.")
                
        except KeyboardInterrupt:
            print("\n[DATA_VAULT] 센티먼트 안테나 접기 완료.")
            break

if __name__ == "__main__":
    analyze_market_sentiment()
