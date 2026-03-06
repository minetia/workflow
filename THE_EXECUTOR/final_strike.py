import time
import json
import os
import random

def execute_final_strike(action, target, amount, is_master_approved=False):
    """
    [THE_EXECUTOR] 
    주군의 통제에 따라 최말단에서 매수/매도를 집행하는 기관
    """
    print("=========================================")
    print(" [THE_EXECUTOR] 레이저 타격 승인 확인소 ")
    print("=========================================")
    
    if not is_master_approved:
        print("⚠️ [THE_EXECUTOR] 거부됨: 주군(MASTER)의 승인 코드가 없습니다.")
        return False
        
    print(f"\n⚡ [THE_EXECUTOR] 통제 반경에 들어왔습니다! 집행 시작:")
    print(f"   ▶ 작전방향 : {action}")
    print(f"   ▶ 목표물   : {target}")
    print(f"   ▶ 타격투입 : {amount} 자본")
    
    time.sleep(1.5) # API 호출 딜레이 시뮬레이션
    
    # 국고 수익에 추가
    profit = round(random.uniform(5.0, 50.0), 2)
    profit_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rank_data', 'imperial_profit.json'))
    
    try:
        if os.path.exists(profit_file):
            with open(profit_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"total_profit": 50000000, "currency": "USDT"}
            
        data["total_profit"] += profit
        data["last_updated"] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        
        with open(profit_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
        print(f"✅ [THE_EXECUTOR] 타격 완수! [{target}] 작전 수익: {profit} USDT")
        print(f"💰 국고 잔고 업데이트: {data['total_profit']:,.2f} USDT\n")
        return True
        
    except Exception as e:
        print(f"🚨 [THE_EXECUTOR] 집행 중 오류 발생: {e}")
        return False

if __name__ == "__main__":
    # 단독 테스트
    execute_final_strike("BUY_DIP", "BTC/USDT", 2.5, True)
