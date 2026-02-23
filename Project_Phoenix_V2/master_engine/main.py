import os
import requests
import pyupbit
from datetime import datetime

# 1. 주군의 전령(송봇) 설정 - 알려주신 정보를 그대로 심었습니다.
TELEGRAM_TOKEN = "8555519110:AAFr6gKhN-t-dIfsU9_4f1zeaV-35bELkYM"
TELEGRAM_CHAT_ID = "1107103330"

# 2. 업비트 보안키 - GitHub Secrets 금고에서 자동으로 꺼내옵니다.
UPBIT_ACCESS = os.getenv("UPBIT_ACCESS_KEY")
UPBIT_SECRET = os.getenv("UPBIT_SECRET_KEY")

def send_telegram_report(message):
    """주군의 송봇(SongBot)에게 전령을 보냅니다."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"보고 실패: {e}")

def run_phoenix_engine():
    """피닉스 V2 엔진 메인 가동 로직"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 보고서 작성
    report = f"🦅 **Project Phoenix V2 가동 보고**\n"
    report += f"------------------------------------\n"
    report += f"📅 **일시**: {now}\n"
    report += f"🛡️ **상태**: 엔진 정상 기동 완료\n"

    # 업비트 잔고 확인
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
    
    # 송봇으로 전송
    send_telegram_report(report)

if __name__ == "__main__":
    try:
        run_phoenix_engine()
    except Exception as e:
        send_telegram_report(f"❌ **엔진 비상 상황**: {e}")
