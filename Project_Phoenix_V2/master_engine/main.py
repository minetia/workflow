import requests
from datetime import datetime

# 1. 주군의 전령(송봇) 설정
TELEGRAM_TOKEN = "8555519110:AAFr6gKhN-t-dIfsU9_4f1zeaV-35bELkYM"
TELEGRAM_CHAT_ID = "1107103330"

def send_telegram_report(message):
    """주군의 송봇(SongBot)에게 전령을 보냅니다."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("주군, 보고를 성공적으로 올렸습니다.")
        else:
            print(f"보고 실패: {response.text}")
    except Exception as e:
        print(f"통신 오류 발생: {e}")

def run_test_mode():
    """업비트 연동 전 통신 확인용 테스트 엔진"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = f"🦅 **Project Phoenix V2 [통신 점검 보고]**\n"
    report += f"------------------------------------\n"
    report += f"📅 **일시**: {now}\n"
    report += f"🛡️ **상태**: 시스템 시동 완료 (테스트 모드)\n"
    report += f"📊 **보고**: 텔레그램 통신망 정상 확인\n"
    report += f"------------------------------------\n"
    report += f"주군, 업비트 연결 없이 정찰 보고를 마칩니다!"
    
    send_telegram_report(report)

if __name__ == "__main__":
    run_test_mode()
