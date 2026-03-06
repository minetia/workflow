# -*- coding: utf-8 -*-
import requests

class PhoenixMessenger:
    def __init__(self):
        self.name = "PHOENIX-Q [Messenger]"
        self.token = "8555519110:AAG9oeqOxQxoMkt_g3DBLdop9GrkaVOad68"
        self.chat_id = "1107103330"
        print(f"🛰️ [{self.name}] 통신 채널 준비 완료.")

    def send_message(self, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": f"🏛️ [PHOENIX EMPIRE]\n{text}",
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, data=payload)
            # 🚀 여기서 'status_code'로 정확히 수정했습니다!
            if response.status_code == 200: 
                print(f"✅ [{self.name}] 보고 완료.")
            else:
                print(f"⚠️ [{self.name}] 통신 오류: {response.text}")
        except Exception as e:
            print(f"🚨 [{self.name}] 치명적 통신 실패: {e}")

if __name__ == "__main__":
    messenger = PhoenixMessenger()
    messenger.send_message("🚀 [PHOENIX] 통신망 수리 완료! 이제 정상적으로 보고를 올립니다.")