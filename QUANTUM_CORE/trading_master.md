# ⚔️ PHOENIX EMPIRE: Trading Master Document

최고 사령관님을 위한 제국 통합 트레이딩 전략 및 매뉴얼입니다. 본 문서는 `ai_4d_trading_engine.py`와 실시간 연동되는 퀀텀 트레이딩의 정수를 담고 있습니다.

## 1. 개요 (Overview)
제국의 트레이딩 시스템은 단순한 매매를 넘어, **양자 지능(Quantum Intelligence)**과 **4차원 시각화(4D Visualization)**를 결합하여 시장의 변동성을 제국의 자산으로 전환합니다.

## 2. 핵심 로직 (Core Logic: AI 4D Engine)
- **AI 분석 레이어**: `backend/indicator_engine.py`가 생성한 기술적 지표를 기반으로 AI 페르소나가 매매 여부를 결정합니다.
- **실시간 리스크 관리**: `backend/security_enforcer.py`와 연동되어 급격한 시장 하락 시 즉시 `PANIC` 모드를 가동, 자산을 보호합니다.
- **4D 엔진**: `backend/ai_4d_trading_engine.py`는 가격 순환, 거래량 압력, 변동성 곡선을 4차원 데이터로 처리하여 최적의 진입점을 추적합니다.

## 3. 사령관 관제 인터페이스 (Command Interface)
- **4D 실시간 트레이딩실 (`/trading_4d`)**:
    - 실시간 캔들 및 AI 의사결정 로그 시각화.
    - 현재 보유 자산 및 실시간 PNL 표시.
- **트레이딩 허가 센터 (`/trading_permit`)**:
    - AI 에이전트의 매매 권한 부여 및 회수.
    - 거래 한도 및 리스크 파라미터 설정.

## 4. API 엔드포인트 (API Endpoints)
- `GET /api/trading/status`: 현재 활성화된 트레이딩 세션 및 AI 상태 조회.
- `GET /api/trading/logs`: AI의 최근 매매 의사결정 로그 및 결과 확인.
- `POST /api/trading/action`: 사령관 직권 매수/매도 명령 하달.

## 5. 보안 및 안전 (Security & Safety)
> [!IMPORTANT]
> 모든 트레이딩 활동은 `PHOENIX_VAULT`의 승인 하에 이루어지며, 제국 금고의 안전이 최우선입니다. `PANIC` 버튼 클릭 시 즉시 모든 원격 거래가 봉쇄됩니다.

사령관님의 무궁한 영광과 제국의 번영을 위하여.
