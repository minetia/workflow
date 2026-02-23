import requests
from datetime import datetime

# 1. 주군의 송봇(SongBot) 설정 - 알려주신 정보를 그대로 이식했습니다.
TELEGRAM_TOKEN = "8555519110:AAFr6gKhN-t-dIfsU9_4f1zeaV-35bELkYM"
TELEGRAM_CHAT_ID = "1107103330"

def send_report(message):
    """주군의 스마트폰으로 즉시 보고를 올립니다."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"보고 실패: {e}")

def run_engine():
    """피닉스 V2 엔진 시동 로직"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = f"🦅 **Project Phoenix V2 시동 성공**\n"
    report += f"------------------------------------\n"
    report += f"📅 **일시**: {now}\n"
    report += f"🛡️ **상태**: 엔진 정상 기동 완료\n"
    report += f"------------------------------------\n"
    report += f"주군, 요새가 이제 정상 작동합니다!"
    
    send_report(report)

if __name__ == "__main__":
    run_engine()
