import os
import time
import sys

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header():
    print("="*60)
    print("      👑 PHOENIX EMPIRE - SUPREME COMMAND DASHBOARD 👑      ")
    print("="*60)
    print(f" [SYSTEM TIME] {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(" [OPERATOR]    PHOENIX COMMANDER")
    print("="*60)

def check_sector(name, path):
    status = "🟢 ONLINE" if os.path.exists(path) else "🔴 OFFLINE"
    print(f" Sector: {name:<10} | Status: {status}")

def main():
    while True:
        clear_console()
        show_header()
        
        print("\n [SECTOR INTEGRITY REPORT]")
        check_sector("EMPIRE", "C:/lovesoong/Empire")
        check_sector("NEXUS", "C:/lovesoong/Nexus")
        check_sector("CORE", "C:/lovesoong/Core")
        check_sector("ZION", "C:/lovesoong/Zion")
        check_sector("ALPHA", "C:/lovesoong/Alpha")
        
        print("\n" + "-"*60)
        print(" 1. Nexus Bridge Control (API Status)")
        print(" 2. Spiritual Monitor (System Health)")
        print(" 3. Vault Protector (Security)")
        print(" 4. Evolution Genesis (Alpha Channel)")
        print(" 0. System Standby (Exit)")
        print("-"*60)
        
        choice = input("\n 하달하실 명령을 선택하십시오: ")
        
        if choice == '0':
            print("\n [System] 제국 시스템을 대기 상태로 전환합니다. 사령관님, 편히 쉬십시오.")
            break
        elif choice == '1':
            print("\n [Nexus] 브릿지 연결을 시도합니다...")
            time.sleep(1)
            # Future: Execute Nexus Bridge logic
        else:
            print("\n [Error] 유효하지 않은 명령입니다.")
            time.sleep(1)

if __name__ == "__main__":
    main()
