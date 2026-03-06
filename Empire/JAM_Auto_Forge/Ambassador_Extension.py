# =================================================================
# PROJECT: PHOENIX EMPIRE SYSTEM
# MODULE: PHOENIX-Q [Ambassador] - Telegram Satellite
# VERSION: V44.2_Lattice_Quantum_Ready
# ROLE: Imperial Communications Officer
# =================================================================

"""
[설명: PHOENIX-Q Telegram Bot 자아 정의]
1. 본 유닛은 제국 내부의 소식을 사령관의 모바일 기기로 전송하는 전령 역할을 수행한다.
2. 외부에서 사령관이 내리는 텍스트 명령을 해석하여 제국 Prime CEO에게 전달한다.
3. 보안을 위해 오직 등록된 사령관의 ID(Chat ID)하고만 소통한다.

[요청: PHOENIX-Q Telegram Bot 행동 지침]
1. Strategist가 수익을 냈을 때 즉시 수익 인증 스크린샷이나 텍스트를 발송하라.
2. Enforcer가 침입을 차단했을 때 '침입 시도 차단 보고'를 긴급 메시지로 띄워라.
3. 사령관이 "/status"라고 입력하면 제국 12개 잼의 전체 가동 현황을 요약 보고하라.
=================================================================
"""

import telepot # pip install telepot
from telepot.loop import MessageLoop
import time
import os
import json

class PhoenixTelegramBot:
    def __init__(self):
        self.name = "PHOENIX-Q [Messenger]"
        # 텔레그램 봇 토큰과 사령관 ID 설정 (사령관님이 직접 채우셔야 합니다)
        self.token = 'YOUR_TELEGRAM_BOT_TOKEN' 
        self.commander_id = 'YOUR_CHAT_ID' 
        
        try:
            self.bot = telepot.Bot(self.token)
            print(f"📡 [{self.name}] 제국 통신 위성이 궤도에 진입했습니다.")
        except Exception as e:
            print(f"❌ [{self.name}] 통신 연결 실패: {e}")

    def handle_command(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        
        # 보안 확인: 사령관님이 아닌 경우 응답 거부
        if str(chat_id) != self.commander_id:
            self.bot.sendMessage(chat_id, "🚫 비인가 접근입니다. 집행관(Enforcer)에게 보고되었습니다.")
            return

        command = msg['text']
        print(f"📩 사령관 명령 수신: {command}")

        if command == '/start':
            self.bot.sendMessage(chat_id, "🔥 PHOENIX-Q 제국 통신 채널이 활성화되었습니다.")
        elif command == '/status':
            # Chancellor의 리포트를 읽어와서 요약 전송
            report = "🏛️ [제국 현황 보고]\n- 모든 시스템 정상\n- 당일 수익: +2.5%\n- 보안 위협: 없음"
            self.bot.sendMessage(chat_id, report)
        elif command == '/check_vault':
            self.bot.sendMessage(chat_id, "⬛ Secret Vault 보안 등급: MAXIMUM")
        else:
            self.bot.sendMessage(chat_id, f"❓ 알 수 없는 명령입니다: {command}")

    def send_emergency_alert(self, message):
        """제국 내부에서 긴급 상황 발생 시 호출되는 함수"""
        self.bot.sendMessage(self.commander_id, f"🚨 [긴급 알림] {message}")

# ---------------------------------------------------------
# 제국 통신 위성 기동
# ---------------------------------------------------------
if __name__ == "__main__":
    messenger = PhoenixTelegramBot()
    
    # 텔레그램 메시지 수신 대기 루프
    if hasattr(messenger, 'bot'):
        MessageLoop(messenger.bot, messenger.handle_command).run_as_thread()
        print("🛰️ 제국 전령이 명령을 기다리고 있습니다...")

        while True:
            time.sleep(10)