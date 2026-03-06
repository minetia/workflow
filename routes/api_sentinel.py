from flask import Blueprint, jsonify
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

sentinel_bp = Blueprint('sentinel', __name__)

BASE_DIR = Path("C:/Users/loves/workflow")

SCAN_TARGETS = {
    "MD": {
        "glob": "**/*.md",
        "dirs": [BASE_DIR, BASE_DIR / "QUANTUM_CORE", BASE_DIR / "PHOENIX_MINING",
                 BASE_DIR / "DATA_VAULT", BASE_DIR / "back", BASE_DIR / "jam",
                 BASE_DIR / "korea"],
    },
    "PY": {
        "glob": "**/*.py",
        "dirs": [BASE_DIR / "backend", BASE_DIR / "routes", BASE_DIR / "data",
                 BASE_DIR / "jam"],
    },
    "JAM": {
        "glob": "*.py",
        "dirs": [BASE_DIR / "jam"],
    }
}

ANOMALY_PATTERNS = ["Empire_Chronicle.md", "Imperial_Report_"]
ACTIVE_HOURS = 6

def classify_file(filepath: Path) -> dict:
    try:
        stat = filepath.stat()
        mtime = datetime.fromtimestamp(stat.st_mtime)
        now = datetime.now()
        delta = now - mtime
        info = {
            "name": filepath.name, "path": str(filepath.relative_to(BASE_DIR)),
            "size": stat.st_size, "modified": mtime.strftime("%Y-%m-%d %H:%M:%S"),
            "minutes_ago": int(delta.total_seconds() / 60),
            "status": "white", "status_label": "정지", "detail": ""
        }
        for pattern in ANOMALY_PATTERNS:
            if pattern in filepath.name:
                info["status"] = "red"; info["status_label"] = "이상 탐지"
                info["detail"] = f"⚠️ 자동 생성 MD 감지: {filepath.name}"; return info
        if mtime.hour < 5:
            info["status"] = "red"; info["status_label"] = "심야 수정"
            info["detail"] = f"⚠️ 새벽 {mtime.hour:02d}:{mtime.minute:02d} 수정 감지"; return info
        if delta <= timedelta(hours=ACTIVE_HOURS):
            info["status"] = "blue"; info["status_label"] = "작업 완료"
            info["detail"] = f"✅ {int(delta.total_seconds() / 60)}분 전 수정"; return info
        info["status"] = "white"; info["status_label"] = "정지"
        info["detail"] = f"💤 마지막 수정: {mtime.strftime('%m/%d %H:%M')}"; return info
    except: return {"name": filepath.name, "status": "red", "status_label": "접근 오류"}

def scan_files(category: str, config: dict) -> list:
    results = []; seen = set()
    for scan_dir in config["dirs"]:
        if not scan_dir.exists(): continue
        try:
            for filepath in scan_dir.glob(config["glob"]):
                if filepath in seen: continue
                if "backup" in str(filepath) or ".git" in str(filepath): continue
                seen.add(filepath)
                item = classify_file(filepath); item["category"] = category; results.append(item)
        except: pass
    return results

@sentinel_bp.route('/api/sentinel/scan')
def sentinel_scan():
    report = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "categories": {}}
    md_files = scan_files("MD", SCAN_TARGETS["MD"])
    py_files = scan_files("PY", {"glob": "*.py", "dirs": [BASE_DIR / "backend", BASE_DIR / "routes", BASE_DIR / "data"]})
    jam_files = scan_files("JAM", SCAN_TARGETS["JAM"])
    for cat, files in [("MD", md_files), ("PY", py_files), ("JAM", jam_files)]:
        report["categories"][cat] = {
            "files": sorted(files, key=lambda x: x["minutes_ago"]),
            "total": len(files),
            "blue": sum(1 for f in files if f["status"] == "blue"),
            "red": sum(1 for f in files if f["status"] == "red"),
            "white": sum(1 for f in files if f["status"] == "white"),
        }
    all_red = [f for cat in report["categories"].values() for f in cat["files"] if f["status"] == "red"]
    report["alert_count"] = len(all_red); report["alerts"] = [f["detail"] for f in all_red]
    return jsonify(report)

@sentinel_bp.route('/sentinel')
def sentinel_dashboard():
    from flask import render_template
    return render_template('PHOENIX_MASTER/sentinel_dashboard.html')
