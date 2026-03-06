from flask import Blueprint, render_template, jsonify, request, session
import time
import os
from .shared import phoenix_members, surrender_list, verdict_history
from backend.ai_persona_engine import phoenix_trader
from backend.security_enforcer import security_enforcer
from backend.vault_encryption import vault_encryption
from backend.vault_manager import vault_manager
from backend.route_sync import route_sync
from backend.backup_engine import imperial_backup_engine

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    return render_template('PHOENIX_MASTER/admin_dashboard.html', 
                          members=phoenix_members, 
                          surrender_list=surrender_list,
                          verdicts=verdict_history)

@admin_bp.route('/judiciary')
def judiciary_hub():
    return render_template('admin_dashboard.html', 
                          active_tab='judiciary',
                          verdicts=verdict_history)

@admin_bp.route('/api/judiciary/anomalies')
def get_judiciary_anomalies():
    import random
    anomalies = []
    for member in phoenix_members:
        score = random.randint(0, 100)
        if score > 80:
            anomalies.append({
                "target": member,
                "score": score,
                "threat_level": "CRITICAL" if score > 90 else "WARNING"
            })
    return jsonify({"status": "SUCCESS", "anomalies": anomalies})

@admin_bp.route('/api/judiciary/execute', methods=['POST'])
def judiciary_execute():
    data = request.json
    target = data.get('target')
    sentence = data.get('sentence', 'WARNING')
    
    if not target:
        return jsonify({"status": "ERROR", "message": "집행 대상을 특정하십시오."}), 400
        
    new_verdict = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "target": target,
        "sentence": sentence.upper(),
        "reason": "Executive Order by Commander"
    }
    verdict_history.append(new_verdict)
    return jsonify({"status": "SUCCESS", "verdict": new_verdict})

@admin_bp.route('/api/admin/sync_routes')
def api_sync_routes():
    role = session.get('role')
    success = route_sync.sync()
    return jsonify({"success": success, "message": "Imperial Route synchronized."})

@admin_bp.route('/api/admin/backup/status')
def backup_status():
    return jsonify(imperial_backup_engine.get_status())

@admin_bp.route('/api/admin/backup/trigger', methods=['POST'])
def trigger_backup():
    result = imperial_backup_engine.trigger_backup_async()
    return jsonify(result)
