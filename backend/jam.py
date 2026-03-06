# -*- coding: utf-8 -*-
"""
# ────────── [ PHOENIX EMPIRE: BACKEND CORE JAM ] ────────────
# PHASE 7: THE ARCHMAGE - INTELLIGENCE & ECONOMY CORE
# ─────────────────────────────────────────────────────────────
# [MODULE] Backend Master Jam (The Archmage)
# [VERSION] 2.2.0 (COMMANDER INTEGRATED)
# [ROLE] 제국 지휘권 행사 및 자산 유동성 관리
# ─────────────────────────────────────────────────────────────
"""
import os
import json
import logging
import datetime

# 제국 내부 보급 부서 소환
from backend.phoenix_vault import phoenix_vault
from backend.matching_engine import matching_engine

logger = logging.getLogger("PHOENIX.BACKEND_CORE")

class BackendMasterJam:
    def __init__(self):
        self.name = "Archmage_Backend_Jam"
        self.vault = phoenix_vault()
        self.engine = matching_engine()
        self.ledger_path = "C:/Users/loves/workflow/data/master_ledger.json"
        
        # [추가] 가동 중인 요원들의 참조 주소를 저장하는 저장소
        self.active_jams = {}
        
        print(f"⚙️ [{self.name}] 제국 경제 코어 및 지휘 통제실이 활성화되었습니다.")

    # ─────────────────────────────────────────────────────────────
    # [명령 하달 섹션] 사령관님의 직통 명령 처리
    # ─────────────────────────────────────────────────────────────
    def dispatch_command(self, raw_command):
        """
        [지시] 사령관님의 명령을 분석하여 특정 요원에게 하달하라.
        예: "/Sniper target BTC" -> Sniper 요원에게 BTC 타격 명령
        """
        parts = raw_command.split()
        if len(parts) < 2:
            return "🚨 명령 형식이 잘못되었습니다. [요원명] [액션] 순으로 입력하십시오."

        jam_name = parts[0].lower().replace("/", "") # 슬래시 제거 처리
        action = parts[1].lower()
        params = parts[2:] if len(parts) > 2 else []

        print(f"📡 [Archmage] {jam_name} 요원에게 '{action}' 명령 하달 중...")

        # 요원별 개별 조종 분기 (라우팅)
        if "sniper" in jam_name:
            return self.sniper_direct_order(action, params)
        elif "collector" in jam_name:
            return self.collector_direct_order(action, params)
        elif "guardian" in jam_name:
            return self.guardian_direct_order(action, params)
        else:
            return f"❓ {jam_name}이라는 요원은 제국 명부에 없습니다."

    def sniper_direct_order(self, action, params):
        if action == "target":
            return f"🎯 [Sniper] 목표를 {params[0]}로 고정했습니다!"
        if action == "stop":
            return "🚫 [Sniper] 저격 중지, 대기 모드 진입."
        return f"❓ Sniper가 '{action}' 명령을 이해하지 못했습니다."

    def collector_direct_order(self, action, params):
        """트리(로그) 요동 방지 및 수집 제어"""
        if action == "mute":
            return "🔇 [Collector] 보고 중단. 이제 트리가 조용해질 것입니다."
        if action == "slow":
            return "🐢 [Collector] 수집 주기 연장. 데이터 흐름을 늦춥니다."
        if action == "resume":
            return "🔊 [Collector] 수집 및 보고 정상 재개."
        return f"📊 [Collector] 수집 명령 '{action}' 수신 완료."

    def guardian_direct_order(self, action, params):
        if action == "shield_up":
            return "🛡️ [Guardian] 방어 레벨 MAX. 보수적 매매 모드 가동."
        return f"🛡️ [Guardian] 보안 명령 '{action}' 수신."

    # ─────────────────────────────────────────────────────────────
    # [경제 관리 섹션] 기존 자산 관리 로직
    # ─────────────────────────────────────────────────────────────
    def process_trade_result(self, trade_data):
        profit = trade_data.get('profit', 0)
        self.vault.deposit(profit)
        self.update_master_ledger(trade_data)
        print(f"💰 [Archmage] 전리품 {profit:,.2f} USD가 제국 금고에 입고되었습니다.")
        return True

    def update_master_ledger(self, entry):
        try:
            current_data = []
            if os.path.exists(self.ledger_path):
                with open(self.ledger_path, 'r', encoding='utf-8') as f:
                    current_data = json.load(f)
            entry['recorded_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_data.append(entry)
            with open(self.ledger_path, 'w', encoding='utf-8') as f:
                json.dump(current_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"장부 기록 실패: {e}")

    def get_imperial_balance(self):
        return self.vault.get_balance()

if __name__ == "__main__":
    # 마스터 잼 가동 테스트
    archmage = BackendMasterJam()
    # 사령관님의 명령 시뮬레이션
    print(archmage.dispatch_command("/Collector mute"))
    print(archmage.dispatch_command("/Sniper target ETH"))