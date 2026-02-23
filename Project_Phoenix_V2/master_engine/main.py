name: Phoenix_Auto_Trade_v2
on:
  schedule:
    - cron: '0 * * * *' # 매시간 정시 실행
  workflow_dispatch:    # 수동 실행 버튼 활성화
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 파이썬 설정
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: 라이브러리 설치
        run: pip install -r requirements.txt
      - name: 엔진 가동
        env:
          UPBIT_ACCESS_KEY: ${{ secrets.UPBIT_ACCESS_KEY }}
          UPBIT_SECRET_KEY: ${{ secrets.UPBIT_SECRET_KEY }}
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        # 주군, 아래 경로를 끝까지 정확히 적었습니다.
        run: python Project_Phoenix_V2/master_engine/main.py
