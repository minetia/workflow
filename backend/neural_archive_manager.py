import os
import zipfile
import json
from datetime import datetime

class NeuralArchiveManager:
    """제국 뉴럴 아카이브 관리자: 대화 기억 및 시스템 로그 보존 담당"""
    def __init__(self):
        self.brain_path = r"C:\Users\loves\.gemini\antigravity\brain\88566b80-d4fd-4420-9a4c-b3af917c7f68"
        self.vault_path = r"C:\Users\loves\workflow\DATA_VAULT\NEURAL_ARCHIVE"
        os.makedirs(self.vault_path, exist_ok=True)

    def create_snapshot(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"NEURAL_SNAPSHOT_{timestamp}.zip"
        zip_path = os.path.join(self.vault_path, zip_name)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as arc:
            # 브레인 아티팩트 및 로그 수집
            for root, dirs, files in os.walk(self.brain_path):
                for file in files:
                    if not file.endswith('.zip'):
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, self.brain_path)
                        arc.write(full_path, arcname=os.path.join("brain", rel_path))
            
            # 워크플로우 중요 설정 및 로그 수집 (선택적)
            log_dir = r"C:\Users\loves\workflow\logs"
            if os.path.exists(log_dir):
                for root, dirs, files in os.walk(log_dir):
                    for file in files:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, log_dir)
                        arc.write(full_path, arcname=os.path.join("logs", rel_path))

        print(f"Neural Snapshot Created: {zip_path}")
        return zip_path

if __name__ == "__main__":
    manager = NeuralArchiveManager()
    manager.create_snapshot()
