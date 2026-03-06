# File: lovesoong/empire_init.py
import os
import json

def initialize_lovesoong_kingdom():
    print(" [SYSTEM] Initializing lovesoong Agent Kingdom...")
    
    # 1. 에이전트 설정 폴더 생성
    os.makedirs(".agent", exist_ok=True)
    
    # 2. 제국 운영 원칙 주입 (Persona: ServerMaster_MD)
    rules_content = """
    # Empire Rules: lovesoong
    - Role: Autonomous Trading & Dev Agent
    - Master: ServerMaster_MD (Commander)
    - Principle 1: Always prioritize risk management (Stop-loss 2%).
    - Principle 2: All code must be verified through Antigravity Artifacts.
    - Principle 3: Use both Korean and English for communication.
    """
    with open(".agent/rules.md", "w", encoding="utf-8") as f:
        f.write(rules_content)

    # 3. Antigravity Skill 정의 (예시: 시장 시황 브리핑 스킬)
    market_skill = {
        "name": "MarketAnalyst",
        "description": "Analyze BTC/SUI/ONDO market sentiment using Gemini 3.1",
        "instructions": "Browse CoinMarketCap and provide a summary report."
    }
    os.makedirs("skills", exist_ok=True)
    with open("skills/market_skill.json", "w") as f:
        json.dump(market_skill, f, indent=4)

    print(" [SUCCESS] lovesoong Kingdom is ready for Antigravity.")

if __name__ == "__main__":
    initialize_lovesoong_kingdom()