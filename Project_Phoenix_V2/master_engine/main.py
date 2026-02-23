import os
import requests
import pyupbit
from datetime import datetime

# ==========================================
# 1. 주군의 비밀 열쇠 및 송봇(SongBot) 설정
# ==========================================
# 주군이 알려주신 소중한 정보를 엔진에 직접 이식했습니다.
TELEGRAM_TOKEN = "8555519110:AAFr6gKhN-t-dIfsU9_4f1zeaV-35bELkYM"
TELEGRAM_CHAT_ID = "1107103330"

# 업비트 키 (GitHub Settings -> Secrets에 등록하시면 보안이 완벽해집니다)
UPBIT_ACCESS = os.getenv("UPBIT_ACCESS_KEY")
UPBIT_SECRET = os.getenv("UPBIT_SECRET_KEY")

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
    """피닉스 V2 엔진의 핵심 구동 로직"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # [기본 상황판 생성]
    report_msg = f"""
🦅 **Project Phoenix V2 가동 보고**
------------------------------------
📅 **일시**: {now}
🛡️ **상태**: 엔진 정상 시동 완료
📊 **정찰**: 시장 데이터 수집 준비 중
------------------------------------
"""

    # 업비트 잔고 확인 (키가 등록된 경우에만 가동)
    if UPBIT_ACCESS and UPBIT_SECRET:
        try:
            upbit = pyupbit.Upbit(UPBIT_ACCESS, UPBIT_SECRET)
            balances = upbit.get_balances()
            krw_balance = 0
            for b in balances:
                if b['currency'] == 'KRW':
                    krw_balance = float(b['balance'])
            report_msg += f"💰 **잔고**: {krw_balance:,.0f} KRW 확보\n"
        except Exception as e:
            report_msg += f"⚠️ **연결 오류**: 업비트 API 키 설정을 확인하십시오.\n"
    else:
        report_msg += "ℹ️ **알림**: 업비트 키가 아직 금고(Secrets)에 없습니다.\n"

    report_msg += "------------------------------------\n주군, 전선에 이상 없습니다!"
    
    # 텔레그램으로 최종 보고
    send_telegram_report(report_msg)

if __name__ == "__main__":
    print(f"[{datetime.now()}] 피닉스 요새 시동 준비...")
    try:
        run_phoenix_engine()
    except Exception as e:
        error_msg = f"❌ **요새 비상 상황 발생**\n사유: {e}"
        send_telegram_report(error_msg)
