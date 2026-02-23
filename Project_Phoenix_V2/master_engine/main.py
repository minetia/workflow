import os
import requests
import pyupbit
from datetime import datetime

# 1. 주군의 송봇(SongBot) 설정
TELEGRAM_TOKEN = "8555519110:AAFr6gKhN-t-dIfsU9_4f1zeaV-35bELkYM"
TELEGRAM_CHAT_ID = "1107103330"

# 2. 업비트 보안키 (GitHub Secrets에서 가져옴)
UPBIT_ACCESS = os.getenv("UPBIT_ACCESS_KEY")
UPBIT_SECRET = os.getenv("UPBIT_SECRET_KEY")

def send_telegram_report(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"보고 실패: {e}")

def run_phoenix_engine():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = f"🦅 **Project Phoenix V2 가동 보고**\n"
    report += f"------------------------------------\n"
    report += f"📅 **일시**: {now}\n"
    report += f"🛡️ **상태**: 엔진 정상 기동 완료\n"
    if UPBIT_ACCESS and UPBIT_SECRET:
        try:
            upbit = pyupbit.Upbit(UPBIT_ACCESS, UPBIT_SECRET)
            balance = upbit.get_balance("KRW")
            report += f"💰 **잔고**: {balance:,.0f} KRW 확보\n"
        except:
            report += f"⚠️ **연결 오류**: 업비트 키를 확인하십시오.\n"
    else:
        report += f"ℹ️ **안내**: 업비트 키가 아직 미등록 상태입니다.\n"
    report += f"------------------------------------\n주군, 전선에 이상 없습니다!"
    send_telegram_report(report)

if __name__ == "__main__":
    try:
        run_phoenix_engine()
    except Exception as e:
        send_telegram_report(f"❌ **엔진 비상 상황**: {e}")
