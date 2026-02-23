import requests
from datetime import datetime

# 1. 주군의 전령(송봇) 설정 - 주군께서 알려주신 정보를 그대로 심었습니다.
TELEGRAM_TOKEN = "8555519110:AAFr6gKhN-t-dIfsU9_4f1zeaV-35bELkYM"
TELEGRAM_CHAT_ID = "1107103330"

def send_telegram_report(message):
    """주군의 송봇(SongBot)을 통해 실시간 전황을 보고합니다."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("주군, 송봇이 보고를 완료했습니다.")
        else:
            print(f"송봇 통신 실패: {response.text}")
    except Exception as e:
        print(f"보고 중 오류 발생: {e}")

def run_phoenix_engine():
    """피닉스 V2 엔진 [통신 점검 모드]"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 주군의 폰으로 날아갈 보고서 내용입니다.
    report_msg = f"""
🦅 **Project Phoenix V2 시동 성공**
------------------------------------
📅 **일시**: {now}
🛡️ **상태**: 엔진 정상 기동 (정상)
📊 **전령**: 송봇 통신망 확보 완료
------------------------------------
주군, 무인 요새가 이제 명령을 기다립니다!
    """
    
    # 텔레그램으로 최종 보고
    send_telegram_report(report_msg)

if __name__ == "__main__":
    print(f"[{datetime.now()}] 피닉스 요새 시동 준비...")
    try:
        run_phoenix_engine()
    except Exception as e:
        error_msg = f"❌ **요새 비상 상황 발생**\n사유: {e}"
        send_telegram_report(error_msg)
