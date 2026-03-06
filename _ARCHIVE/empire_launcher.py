# File: empire_launcher.py
import os
import subprocess
import sys
import time

def initiate_commander_protocol():
    """
    사령관님의 명령에 따라 Antigravity 실행 파일을 탐색하고 구동함.
    """
    print(" [SYSTEM] Initializing Antigravity Execution Protocol...")
    
    # 1. 예상 경로 리스트 (사령관님의 데이터 기반)
    search_dirs = [
        os.path.join(os.environ['LOCALAPPDATA'], "Antigravity"),
        "C:\\Program Files\\Antigravity",
        "C:\\Users\\loves\\Project_Phoenix",
        "C:\\lovesoong"
    ]
    
    executable_path = None

    # 2. 실행 파일 탐색
    for directory in search_dirs:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                if "Antigravity.exe" in files:
                    executable_path = os.path.join(root, "Antigravity.exe")
                    break
        if executable_path: break

    # 3. 실행 프로세스
    if executable_path:
        print(f" [SUCCESS] Target Acquired: {executable_path}")
        print(" [SYSTEM] Launching Antigravity IDE... Glory to the Empire.")
        
        # 에이전트 모드로 실행 (백그라운드 제어권 확보)
        subprocess.Popen([executable_path, "--agent-mode", "--commander-id=ServerMaster_MD"])
    else:
        print(" [ERROR] 실행 파일을 찾을 수 없습니다. 수동 설치 확인이 필요합니다.")
        print(" [ADVISORY] https://antigravity.google 에서 최신본을 재설치하십시오.")

if __name__ == "__main__":
    initiate_commander_protocol()