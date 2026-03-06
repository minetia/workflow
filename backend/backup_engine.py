import os
import shutil
import zipfile
import threading
from datetime import datetime
from pathlib import Path

# 제국 루트 및 백업 전용 디렉토리 설정
IMPERIAL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_CHAMBER = os.path.join(IMPERIAL_ROOT, "BACKUP_CHAMBER")
LOCAL_BACKUP_DIR = os.path.join(IMPERIAL_ROOT, "backup") # 사령관 전용 ./backup 폴더

# 보존할 최대 백업 일수 (제국 율령 14일)
MAX_RETENTION_DAYS = 14

class BackupEngine:
    def __init__(self) -> None:
        self.status: str = "IDLE"
        self.last_backup_time: str | None = None
        self.last_backup_file: str | None = None
        self.max_retention = MAX_RETENTION_DAYS
        self.ensure_chamber_exists()
        self._start_auto_mgmt_thread()

    def ensure_chamber_exists(self):
        if not os.path.exists(BACKUP_CHAMBER):
            os.makedirs(BACKUP_CHAMBER)
        if not os.path.exists(LOCAL_BACKUP_DIR):
            os.makedirs(LOCAL_BACKUP_DIR)

    def trigger_backup_async(self):
        """백업 프로세스를 비동기(백그라운드 스레드)로 실행합니다."""
        if self.status == "RUNNING":
            return {"success": False, "message": "백업이 이미 진행 중입니다."}
            
        thread = threading.Thread(target=self._run_backup_process)
        thread.start()
        
        # 주군의 명에 따라 로컬 ./backup 동기화도 함께 수행
        self.trigger_sync_async()
        
        return {"success": True, "message": "제국 데이터 백업 및 ./backup 동기화 시퀀스가 시작되었습니다."}

    def trigger_sync_async(self):
        """./backup 폴더로의 실시간 동기화를 비동기로 실행합니다."""
        thread = threading.Thread(target=self._run_sync_process)
        thread.start()
        return {"success": True, "message": "./backup 동기화 시작"}

    def _run_backup_process(self):
        self.status = "RUNNING"
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"IMPERIAL_BACKUP_v_{timestamp}.zip"
            backup_path = os.path.join(BACKUP_CHAMBER, backup_filename)

            # 압축할 핵심 코어 디렉토리 목록
            core_targets = [
                "PHOENIX_MASTER",
                "backend",
                "DATA_VAULT",
                "data",
                "QUANTUM_CORE"
            ]

            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for target in core_targets:
                    target_dir = os.path.join(IMPERIAL_ROOT, target)
                    if os.path.exists(target_dir):
                        for root, dirs, files in os.walk(target_dir):
                            # __pycache__ 나 node_modules 같은 찌꺼기는 백업 제외 (선택적)
                            if '__pycache__' in dirs:
                                dirs.remove('__pycache__')
                            for file in files:
                                if file.endswith('.pyc') or file.endswith('.log'):
                                    continue
                                
                                file_path = os.path.join(root, file)
                                # 백업 파일 내부에서의 상대 경로 계산 (ex: PHOENIX_MASTER/index.html)
                                rel_path = os.path.relpath(file_path, IMPERIAL_ROOT)
                                zipf.write(file_path, rel_path)

            self.last_backup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.last_backup_file = backup_filename
            
            # 성공 후 오래된 백업 정리 (정화소 연계)
            self._purify_old_backups()
            
            self.status = "COMPLETED"
        except Exception as e:
            self.status = f"FAILED: {str(e)}"

    def _run_sync_process(self):
        """./backup 폴더로 현재 프로젝트의 모든 파일을 복사(동기화)합니다."""
        try:
            # 동기화할 대상 (루트의 모든 주요 파일 및 폴더)
            for item in os.listdir(IMPERIAL_ROOT):
                # 자기 자신(backup 폴더)과 대용량 찌꺼기는 제외
                if item in ['backup', 'BACKUP_CHAMBER', 'NETWORK_DIVISION', '.git', '__pycache__', 'venv', '.env', 'node_modules']:
                    continue
                
                src = os.path.join(IMPERIAL_ROOT, item)
                dst = os.path.join(LOCAL_BACKUP_DIR, item)

                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.log'))
                else:
                    shutil.copy2(src, dst)
            
            print(f"[BACKUP_ENGINE] {datetime.now()} - ./backup 동기화 완료")
        except Exception as e:
            print(f"[BACKUP_ENGINE] 동기화 오류: {e}")

    def restore_backup(self, filename: str):
        """지정된 백업 파일을 사용하여 시스템을 복구합니다."""
        backup_path = os.path.join(BACKUP_CHAMBER, filename)
        if not os.path.exists(backup_path):
            return {"success": False, "message": "백업 파일을 찾을 수 없습니다."}

        # 1. 안전을 위해 현재 상태 선행 백업
        self._run_backup_process()
        
        try:
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # 필터링 없이 Imperial Root에 덮어쓰기 (주의 필요)
                zipf.extractall(IMPERIAL_ROOT)
            
            return {"success": True, "message": f"[{filename}] 스냅샷으로 시스템 복구가 완료되었습니다. 서비스를 재시작하십시오."}
        except Exception as e:
            return {"success": False, "message": f"복구 중 오류 발생: {str(e)}"}

    def _start_auto_mgmt_thread(self):
        """6시간마다 자동 정화를 수행하는 데몬 스레드 구동"""
        def mgmt_loop():
            while True:
                self._purify_old_backups()
                time.sleep(21600) # 6 hours

        import time
        t = threading.Thread(target=mgmt_loop, daemon=True)
        t.start()

    def _purify_old_backups(self):
        """MAX_RETENTION_DAYS 보다 오래된 백업 파일을 소각(삭제)합니다."""
        now = datetime.now()
        for filename in os.listdir(BACKUP_CHAMBER):
            if filename.startswith("IMPERIAL_BACKUP_v_") and filename.endswith(".zip"):
                filepath = os.path.join(BACKUP_CHAMBER, filename)
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                age_days = (now - file_time).days
                if age_days > self.max_retention:
                    try:
                        os.remove(filepath)
                        print(f"[BACKUP_PURGE] {filename} 소각 완료 (Retention Policy: {self.max_retention}일)")
                    except:
                        pass

    def set_retention_days(self, days: int):
        self.max_retention = days
        return {"success": True, "message": f"보존 정책이 {days}일로 변경되었습니다."}

    def get_status(self):
        # 현재 저장된 백업 파일 목록(시간 역순 정렬)
        backup_files = []
        if os.path.exists(BACKUP_CHAMBER):
            files = [f for f in os.listdir(BACKUP_CHAMBER) if f.endswith('.zip')]
            files.sort(key=lambda x: os.path.getmtime(os.path.join(BACKUP_CHAMBER, x)), reverse=True)
            for f in files:
                fpath = os.path.join(BACKUP_CHAMBER, f)
                size_mb = os.path.getsize(fpath) / (1024 * 1024)
                backup_files.append({
                    "name": f,
                    "date": datetime.fromtimestamp(os.path.getmtime(fpath)).strftime("%Y-%m-%d %H:%M:%S"),
                    "size": f"{size_mb:.2f} MB"
                })

        return {
            "status": self.status,
            "last_backup_time": self.last_backup_time,
            "archives": backup_files,
            "chamber_path": BACKUP_CHAMBER
        }

# 싱글톤 인스턴스
imperial_backup_engine = BackupEngine()
