import os
import google.generativeai as genai
from dotenv import load_dotenv

class NexusBridge:
    def __init__(self):
        load_dotenv(dotenv_path="C:/Users/loves/workflow/Project_Phoenix/.env")
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("🚨 [Nexus] GEMINI_API_KEY가 존재하지 않습니다. ZION 구역을 확인하십시오.")
            return

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        print("📡 [Nexus] Gemini Intelligence Link Established.")

    def send_imperial_command(self, prompt, instruction="당신은 제국의 충성스러운 조력자입니다."):
        try:
            response = self.model.generate_content(
                f"{instruction}\n\nCommander's Request: {prompt}"
            )
            return response.text
        except Exception as e:
            return f"❌ [Nexus Error] API 통신 실패: {str(e)}"

if __name__ == "__main__":
    bridge = NexusBridge()
    if bridge.api_key:
        print("\n--- [Nexus Communication Test] ---")
        print(bridge.send_imperial_command("제국 인프라의 현재 상태를 한 줄로 요약하라."))
