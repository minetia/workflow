import os
from datetime import datetime
from pathlib import Path

class RouteSync:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.target_file = self.base_dir / "제국루트.txt"
        self.archive_dir = self.base_dir / "LOGS_HISTORY"
        
        # Ensure archive directory exists
        if not self.archive_dir.exists():
            os.makedirs(self.archive_dir, exist_ok=True)
        
        # 제국 용어 사전 (Imperial Dictionary)
        self.descriptions = {
            "main.py": "👑 제국 통합 관제 센터 [피닉스]",
            "index.html": "🏛️ 사령부 심장 - 하사 V44.2 [LV.1]",
            "run_war.bat": "⚡ 무인 기동 엔진 스위치 [피닉스]",
            "strategic_dashboard.html": "📉 웅군술족 전략 대시보드 [LV.3]",
            "PHOENIX_MASTER": "🏢 제국 행정 및 자산 분석 구역 [LV.4]",
            "PHOENIX_HUB": "🌍 제국 글로벌 거래소 허브 구역 [LV.4]",
            "PHOENIX_WALLET": "👛 제국 가상-현실 듀얼 지갑 구역 [LV.1]",
            "PHOENIX_MINING": "💎 제국 양자 채굴 및 교육 구역 [LV.1]",
            "PHOENIX_CIVITAS": "🏙️ 제국 시민 생활 허브 (Park/Market/Housing) [LV.1]",
            "QUANTUM_CORE": "🧬 양자 연산 및 자동 연구 구역 [LV.3]",
            "backend": "⚙️ 제국 7대 마법사 지능 및 경제 코어 [LV.4]",
            "DATA_VAULT": "📂 데이터 저장 및 정렬 구역 [LV.2]",
            "SECURITY_SHIELD": "🛡️ 보안 및 사법 구역 [피닉스]",
            "data": "📊 제국 실시간 DB [LV.4]",
            "templates": "🎨 제국 UI 템플릿 저장소 [LV.4]",
            "static": "📂 제국 정적 자산 로드 구역 [LV.1]",
            # Sub-files
            "navigation.html": "🗺️ 대광장 네비바 [LV.1]",
            "imperial_nav.html": "📜 통합형 임페리얼 네비바 [LV.1]",
            "vault_analytics.html": "📊 금고 정밀 분석 엔진 [LV.1]",
            "global_hub.html": "🌍 글로벌 거래소 통합 관리 센터 [LV.4]",
            "dual_bridge.html": "🌉 사령관 전용 자산 브릿지 [LV.1]",
            "member_list.html": "👥 제국 요원 명부 [LV.2]",
            "pqc_user_manual.md": "📘 PQC 공식 매뉴얼 [LV.1]",
            "research_agents.py": "🤖 양자컴퓨터 형제들 - 자동 연구 [LV.3]",
            "phoenix_vault.py": "💰 제국 금고 정산 엔진 [LV.4]",
            "hub_manager.py": "🌍 허브 통합 관리 시스템 [LV.4]",
            "route_sync.py": "📜 제국 루트 자동 기록관 [피닉스]",
            "civitas_center.html": "🏙️ 시민 생활 허브 포털 [LV.1]",
            "park.html": "🌳 제국 공원 및 교육 세션 [LV.1]",
            "market.html": "🎭 피닉스 플라자 상업 지구 [LV.1]",
            "bank.html": "🏦 퀀텀 금융 개인 센터 [LV.1]",
            "estate.html": "🏰 임페리얼 에스테이트 주거 지구 [LV.1]",
            "IMPERIAL_SECRET_VAULT": "⬛ [극비] 접근 거부 [피닉스]",
            "secret_chronicle.html": "📜 사령관 전용 비밀 연대기 [피닉스]",
            # Korea Hub
            "korea": "🇰🇷 제국 코리아 허브 구역 [LV.4]",
            "ai_trader.py": "🤖 코리아 전용 AI 트레이더 [LV.4]",
            "binance_api.py": "🔌 바이낸스 연동 모듈 [LV.4]",
            "upbit_api.py": "🔌 업비트 연동 모듈 [LV.4]",
            "trading_engine.py": "⚙️ 코리아 통합 매매 엔진 [LV.4]",
            "commander_center.html": "🛰️ 커맨더 센터 통제실 [LV.4]",
            "market_armory.html": "🏛️ 제국 무기고 (Market) [LV.4]",
            "phoenix_command.html": "⚡ 피닉스 지휘 본부 [LV.4]",
            "vault_system.html": "💰 슈프림 금고 레지스트리 [LV.4]",
            "analytics_hub.html": "🧠 분석 및 AI 허브 [LV.4]",
            "global_insight.html": "🌍 글로벌 마켓 인사이트 [LV.4]",
            "market_intel.html": "🔎 마켓 인텔리전스 센터 [LV.4]"
        }

    def _get_description(self, name):
        return self.descriptions.get(name, "제국 가동 자산")

    def generate_tree(self, start_time=None, end_time=None):
        lines = []
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        lines.append(f"┌──────────────────────────────────────────────────────────┐")
        lines.append(f"│ 👑 PHOENIX EMPIRE - IMPERIAL ROUTE DOCUMENTATION         │")
        if start_time:
            lines.append(f"│ [공정 시작] {start_time}")
        if end_time:
            lines.append(f"│ [공정 완료] {end_time}")
        lines.append(f"└──────────────────────────────────────────────────────────┘")
        lines.append("")
        lines.append(f"{self.base_dir} 제국 루트")
        lines.append("│")
        
        # Root level files (prioritized)
        root_files = ["main.py", "index.html", "run_war.bat", "strategic_dashboard.html"]
        for f in root_files:
            if (self.base_dir / f).exists():
                lines.append(f"├── 👑 {f} ({self._get_description(f)})")
        
        lines.append("│")

        # Directories
        target_dirs = [
            "PHOENIX_MASTER", "PHOENIX_HUB", "PHOENIX_WALLET", 
            "PHOENIX_MINING", "PHOENIX_CIVITAS", "QUANTUM_CORE", 
            "backend", "DATA_VAULT", "SECURITY_SHIELD", "data", "korea", "IMPERIAL_SECRET_VAULT"
        ]

        for idx, d_name in enumerate(target_dirs):
            d_path = self.base_dir / d_name
            if d_path.exists():
                is_last_dir = (idx == len(target_dirs) - 1)
                prefix = "└──" if is_last_dir else "├──"
                lines.append(f"{prefix} 📂 {d_name}/ ({self._get_description(d_name)})")
                
                # List files in dir (max 8, hide for secret vault)
                try:
                    if d_name == "IMPERIAL_SECRET_VAULT":
                        lines.append(f"{sub_prefix}└── ⬛ [ENCRYPTED DATA FLOW]")
                        continue
                        
                    files = [f for f in os.listdir(d_path) if os.path.isfile(os.path.join(d_path, f))]
                    for f_idx, f_name in enumerate(files[:8]):
                        sub_prefix = "    " if not is_last_dir else "    "
                        connector = "└──" if (f_idx == len(files[:8]) - 1) else "├──"
                        desc = self._get_description(f_name)
                        lines.append(f"{sub_prefix}{connector} {f_name} ({desc})")
                except:
                    pass
                
                if not is_last_dir:
                    lines.append("│")

        return "\n".join(lines)

    def get_delta(self, old_content: str, new_content: str) -> str:
        """이전 기록과 현재 기록을 비교하여 변동 사항(Delta) 추출"""
        if not old_content:
            return "┌── [INITIAL_BOOT] 제국 루트 최초 기록 수립"

        old_lines = [line.strip() for line in old_content.split('\n') if '──' in line]
        new_lines = [line.strip() for line in new_content.split('\n') if '──' in line]

        added = []
        deleted = []

        # 단순 비교 (트리 구조의 특성상 완전한 diff보다는 행 단위 가독성 중점)
        for line in new_lines:
            if line not in old_lines:
                added.append(f"  [NEW] {line}")
        
        for line in old_lines:
            if line not in new_lines:
                deleted.append(f"  [DEL] {line}")

        delta_report = []
        if added or deleted:
            delta_report.append("┌──────────────────────────────────────────────────────────┐")
            delta_report.append("│ 📊 제국 변동 사항 (IMPERIAL DELTAS)                      │")
            delta_report.append("└──────────────────────────────────────────────────────────┘")
            for item in added:
                delta_report.append(item)
            for item in deleted:
                delta_report.append(item)
            delta_report.append("")
        else:
            delta_report.append("  [NO_CHANGES] 제국 아키텍처 상태 유지 중")

        return "\n".join(delta_report)

    def sync(self):
        try:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 이전 기록 읽기 (Delta 비교용)
            old_content = ""
            if self.target_file.exists():
                with open(self.target_file, "r", encoding="utf-8") as f:
                    old_content = f.read()

            # 현재 트리 생성
            current_tree = self.generate_tree(start_time=start_time, end_time="연산 완료")
            
            # Delta 계산
            delta_section = self.get_delta(old_content, current_tree)
            
            # 최종 문서 조립 (헤더 + 트리 + 델타)
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            final_tree = self.generate_tree(start_time=start_time, end_time=end_time)
            
            full_content = f"{final_tree}\n\n{delta_section}"
            
            # Main update
            with open(self.target_file, "w", encoding="utf-8") as f:
                f.write(full_content)
            
            # Archive update
            archive_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            archive_path = self.archive_dir / f"{archive_timestamp}_제국루트.txt"
            with open(archive_path, "w", encoding="utf-8") as f:
                f.write(full_content)
                
            print(f"[경로 동기화] 제국 루트가 델타와 함께 업데이트되었습니다.")
            return True
        except Exception as e:
            print(f"[ROUTE SYNC ERROR] {e}")
            return False

route_sync = RouteSync()

if __name__ == "__main__":
    route_sync.sync()
