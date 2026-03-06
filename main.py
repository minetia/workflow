import os
import sys
import io

# 🛡️ Force UTF-8 for Windows Terminal Stability (Unicode Emojis)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from flask import render_template
from dotenv import load_dotenv
load_dotenv()

# 🌐 Ensure Imperial Core and Workflow are in path
IMPERIAL_ROOT = r"c:\lovesoong"
WORKFLOW_ROOT = r"C:\Users\loves\workflow"
for root in [IMPERIAL_ROOT, WORKFLOW_ROOT]:
    if root not in sys.path:
        sys.path.append(root)

# 기존 제국 핵심 부품 로드
from backend.app_factory import create_app
from backend.service_orchestrator import start_background_services

# 🛡️ 제국 Flask 애플리케이션 생성
app = create_app()

@app.route('/jam/bybit')
def serve_bybit():
    """바이비트 전용 프로 트레이더 뷰를 출력합니다."""
    return render_template('bybit_live.html')

@app.route('/jam/grid')
def serve_grid():
    """양자 거미줄(Quantum Grid) 전용 통제 화면을 출력합니다."""
    return render_template('quantum_grid.html')

@app.route('/jam/traders')
def serve_traders():
    """100인의 늑대들(Traders)의 실시간 랭킹 리더보드를 출력합니다."""
    return render_template('trader_leaderboard.html')

@app.route('/jam/nexus')
def serve_nexus():
    """제국의 모든 시스템을 한눈에 보고 이동하는 넥서스 허브입니다."""
    return render_template('nexus.html')

@app.route('/jam/commander_center')
def serve_commander():
    """리소스 낭비 없이 제국의 커맨더 센터를 즉시 로드합니다."""
    return render_template('commander_center.html')

@app.route('/jam/gemini2')
def serve_gemini2():
    """제미나이 2.0 인텔리전스 허브를 기동합니다."""
    return render_template('gemini2.html')

@app.route('/')
def index():
    """사용자가 접속하자마자 직관적으로 시스템을 보게 유도합니다."""
    return serve_nexus()

if __name__ == '__main__':
    # 🚀 배경 지능 레이어 가동
    try:
        start_background_services()
    except Exception as e:
        print(f"Background services warning: {e}")

    print("✨ 제국 통합 시스템 가동: http://127.0.0.1:5001/jam/commander_center")
    # Debug 모드를 꺼서 안정성 확보
    app.run(host='0.0.0.0', port=5001, debug=True)
