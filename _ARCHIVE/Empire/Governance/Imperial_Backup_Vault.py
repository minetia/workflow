import os
import shutil
import json
from datetime import datetime

BASE_DIR = r"c:\lovesoong"
BACKUP_DIR = os.path.join(BASE_DIR, "backup")

class ImperialBackupVault:
    """
    🕋 [IMPERIAL BACKUP VAULT] - 제국 자산 보존소
    모든 MD(Master Dept) 및 JAM(Junior Assistant Master) 에이전트들의 코드를 정기적으로 백업합니다.
    """
    def __init__(self):
        self.last_backup_file = os.path.join(BASE_DIR, "data", "last_backup_info.json")

    def execute_supreme_backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        current_backup_path = os.path.join(BACKUP_DIR, timestamp)
        os.makedirs(current_backup_path, exist_ok=True)
        
        print(f"🕋 [BackupVault] 제국 자산 백업 시퀀스 개시: {timestamp}")
        
        backed_up_files = []
        
        # Scan for MD and JAM files
        for root, dirs, files in os.walk(BASE_DIR):
            if "backup" in root or ".git" in root or "__pycache__" in root:
                continue
            
            for file in files:
                if file.startswith("MD_") or file.startswith("JAM_") or "investigator.py" in file or "Architect" in file or "Chancellor" in file or "Strategist" in file:
                    if file.endswith(".py"):
                        src_path = os.path.join(root, file)
                        # Create relative path structure in backup to avoid collisions
                        rel_path = os.path.relpath(root, BASE_DIR)
                        dst_root = os.path.join(current_backup_path, rel_path)
                        os.makedirs(dst_root, exist_ok=True)
                        
                        shutil.copy2(src_path, os.path.join(dst_root, file))
                        backed_up_files.append(os.path.join(rel_path, file))

        # Save record
        record = {
            "timestamp": timestamp,
            "file_count": len(backed_up_files),
            "files": backed_up_files
        }
        with open(self.last_backup_file, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=4)
            
        print(f"✅ [BackupVault] 백업 완료. 총 {len(backed_up_files)}개의 부서 지능이 보존되었습니다.")
        return record

# Global Instance
imperial_backup_vault = ImperialBackupVault()

if __name__ == "__main__":
    imperial_backup_vault.execute_supreme_backup()
