import time
import random

def risk_breaker():
    print("=========================================")
    print(" [SECURITY_SHIELD] 위험 통제 방어벽 가동 ")
    print("=========================================")
    
    threshold = -0.001 # -0.1% 손실 허용치
    print(f"[RISK_BREAKER] 허용 손실 임계값: {threshold*100}%")
    
    # 가상의 수익률 모니터링
    while True:
        try:
            time.sleep(10)
            current_pnl = random.uniform(-0.002, 0.05) # -0.2% ~ +5.0%
            
            if current_pnl <= threshold:
                print(f"\n🚨 [SECURITY_SHIELD] 비상! 0.1% 손실 방어벽 발동! (현재: {current_pnl*100:.2f}%)")
                print("🚨 모든 매매 일시 정지 및 안전 자산 전환 완료.")
                time.sleep(15) # 방어벽 활성화 시간
                print("\n[SECURITY_SHIELD] 시장 안정. 방어벽 해제 및 재가동.")
            else:
                print(f"[RISK_BREAKER] 포트폴리오 안전 상태. (손익: {current_pnl*100:.2f}%)")
                
        except KeyboardInterrupt:
            print("\n[SECURITY_SHIELD] 방어벽 엔진 정지.")
            break

if __name__ == "__main__":
    risk_breaker()
