import json
import os
import time

def sort_ranks():
    print("====================================")
    print(" [DATA_VAULT] 랭크 정렬 모듈 가동 ")
    print("====================================")
    
    rank_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rank_data', 'agent_ranks.json'))
    
    while True:
        try:
            if not os.path.exists(rank_file_path):
                print(f"[DATA_VAULT] 오류: {rank_file_path} 파일이 없습니다.")
                time.sleep(5)
                continue
                
            with open(rank_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 포인트 기준 내림차순 정렬
            sorted_agents = sorted(data.items(), key=lambda x: x[1].get('points', 0), reverse=True)
            
            print(f"\n[{time.strftime('%H:%M:%S')}] --- 실시간 제국 서열 ---")
            for idx, (name, info) in enumerate(sorted_agents):
                print(f"{idx+1}위: {name} (등급: {info.get('level', '알수없음')}, {info.get('points', 0):,} pt)")
            print("---------------------------------")
            
            # 10초마다 재정렬
            time.sleep(10)
            
        except json.JSONDecodeError:
            print("[DATA_VAULT] JSON 파싱 오류. 파일이 손상되었을 수 있습니다.")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n[DATA_VAULT] 정렬 모듈 정지.")
            break

if __name__ == "__main__":
    sort_ranks()
