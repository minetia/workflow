# =================================================================
# PROJECT: PHOENIX EMPIRE SYSTEM
# MODULE: PHOENIX-Q [Steward] Intelligence Core
# VERSION: V44.2_Lattice_Quantum_Ready
# ROLE: Chief Data Steward & DB Integrity Manager
# =================================================================

"""
[설명: PHOENIX-Q Steward 자아 정의]
1. 본 유닛은 제국 전역에서 생성되는 모든 실시간 데이터(JSON)와 로그 파일의 생애주기를 관리한다.
2. 데이터의 파편화(Fragmentation)를 방지하고, 읽기/쓰기 속도를 최적화하기 위한 인덱싱을 수행한다.
3. 모든 데이터가 제국 표준 규격에 맞게 저장되는지 검증하며, 손상된 데이터를 즉시 복구한다.

[요청: PHOENIX-Q Steward 행동 지침]
1. data/ 폴더 내의 모든 JSON 파일이 올바른 문법(Syntax)을 유지하고 있는지 매시간 검사하라.
2. audit_log.json의 크기가 일정 수준을 초과하면 압축(Archive)하여 저장 공간을 확보하라.
3. 각 잼(JAM)들이 생성하는 로그의 형식을 통일하고, 누락된 데이터가 없는지 체크하라.
=================================================================
"""

import os
import json
import datetime
import shutil

class PhoenixQSteward:
    def __init__(self):
        self.name = "PHOENIX-Q [Steward]"
        self.root_path = "C:/Users/loves/workflow/data"
        self.archive_path = os.path.join(self.root_path, "archives")
        self.integrity_log = os.path.join(self.root_path, "steward_ops.log")
        
        if not os.path.exists(self.archive_path):
            os.makedirs(self.archive_path)
            
        print(f"[{self.name}] 데이터베이스 관리 지능이 가동되었습니다.")
        print(f"[{self.name}] 관할 구역: {self.root_path} (제국 중앙 데이터 저장소)")

    # ---------------------------------------------------------
    # [설명] 데이터 무결성 검사 및 정제 지식
    # ---------------------------------------------------------
    def check_json_integrity(self):
        """
        [설명] data/ 폴더 내 모든 .json 파일을 스캔하여 
        손상되거나 문법이 틀린 데이터가 있는지 전수 조사합니다.
        """
        print(f"🔍 [{self.name}] 전체 JSON 데이터 무결성 검사 중...")
        report = {"total": 0, "corrupted": []}
        
        for file in os.listdir(self.root_path):
            if file.endswith(".json"):
                report["total"] += 1
                file_path = os.path.join(self.root_path, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        json.load(f)
                except json.JSONDecodeError:
                    report["corrupted"].append(file)
                    print(f"🚨 [{self.name}] 손상된 파일 발견: {file}")
                    
        return report

    # ---------------------------------------------------------
    # [요청] 대용량 로그 압축 및 데이터 정리 기능
    # ---------------------------------------------------------
    def archive_old_logs(self, threshold_mb=10):
        """
        [요청] 로그 파일의 크기가 설정된 임계치(MB)를 넘으면 
        이를 archives/ 폴더로 이동시키고 새로 시작합니다.
        """
        print(f"📦 [{self.name}] 로그 아카이빙 작업 시작 (임계치: {threshold_mb}MB)...")
        
        for file in os.listdir(self.root_path):
            if file.endswith(".log"):
                file_path = os.path.join(self.root_path, file)
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                
                if size_mb > threshold_mb:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    archive_name = f"{file}.{timestamp}.bak"
                    shutil.move(file_path, os.path.join(self.archive_path, archive_name))
                    print(f"✅ [{self.name}] {file} 압축 완료: {archive_name}")
        
        self._log_ops("Log Archiving Process Completed.")

    # ---------------------------------------------------------
    # [요청] 실시간 데이터 상태 요약 (Health Summary)
    # ---------------------------------------------------------
    def generate_data_health_report(self):
        """현재 제국 데이터 저장소의 전반적인 상태를 요약하여 Chancellor에게 전달합니다."""
        print(f"📊 [{self.name}] 데이터 헬스 리포트 생성 중...")
        report = self.check_json_integrity()
        
        summary = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "health_score": 100 - (len(report["corrupted"]) * 10),
            "total_files": report["total"],
            "status": "Optimal" if not report["corrupted"] else "Maintenance Required"
        }
        
        summary_path = os.path.join(self.root_path, "data_health_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=4)
            
        return summary_path

    def _log_ops(self, message):
        """데이터 관리 활동을 꼼꼼하게 기록합니다."""
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        with open(self.integrity_log, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} {message}\n")

# ---------------------------------------------------------
# 제국 데이터 저장소 관리 기동 영역
# ---------------------------------------------------------
if __name__ == "__main__":
    steward = PhoenixQSteward()
    
    # 1. 무결성 검사 실행
    integrity = steward.check_json_integrity()
    
    # 2. 로그 정리 작업 실행
    steward.archive_old_logs(threshold_mb=5)
    
    # 3. 헬스 리포트 생성
    report_path = steward.generate_data_health_report()
    print(f"✨ 데이터 상태 보고서가 작성되었습니다: {report_path}")