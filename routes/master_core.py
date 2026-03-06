from flask import Blueprint, render_template, jsonify, request
import os, zipfile
import hashlib
import subprocess
import threading
import queue
import time

master_bp = Blueprint('master_core', __name__)
log_queue = queue.Queue()
TARGET_DIR = r"c:\lovesoong" # Updated to new core path
COLORS = ["#00f0ff", "#ff00ff", "#ffff00", "#00ff00", "#ff8000", "#8000ff"]

def get_colored_tree(path, depth=0, prefix="", parent_id="root"):
    tree_html = ""
    try:
        if not os.path.exists(path): return "경로 없음"
        items = sorted(os.listdir(path))
        filtered = [i for i in items if os.path.isdir(os.path.join(path, i)) or i.endswith(('.py', '.md'))]
        
        for i, item in enumerate(filtered):
            full_path = os.path.join(path, item)
            if item == "BACKUP_CHAMBER" or item.startswith('.'): continue
            is_last = (i == len(filtered) - 1)
            connector = "└── " if is_last else "├── "
            item_id = hashlib.md5(full_path.encode()).hexdigest()[:8]
            
            if os.path.isdir(full_path):
                color = COLORS[depth % len(COLORS)]
                tree_html += f'{prefix}{connector}<input type="checkbox" class="group-check" data-id="{item_id}" onclick="checkGroup(this)"> '
                tree_html += f'<span style="color:{color}; font-weight:bold; cursor:pointer;" onclick="toggleTreeGroup(\'{item_id}\')">'
                tree_html += f'<span id="toggle-icon-{item_id}">[-]</span> [GROUP] {item}</span>\n'
                
                tree_html += f'<div id="sub-{item_id}" style="display: block;">'
                tree_html += get_colored_tree(full_path, depth + 1, prefix + ("    " if is_last else "│   "), item_id)
                tree_html += '</div>'
            else:
                tree_html += f'{prefix}{connector}<input type="checkbox" class="unit-check" data-parent="{parent_id}" value="{item}"> <button class="go-btn" onclick="openUnit(\'{item}\')">GO 이동</button> <span class="tree-file">{item}</span>\n'
    except: pass
    return tree_html

@master_bp.route('/master_console')
def master_console():
    tree = get_colored_tree(TARGET_DIR)
    return render_template('master_console.html', tree=tree)

@master_bp.route('/api/master/instruct')
def api_instruct():
    unit = request.args.get('unit')
    cmd = request.args.get('cmd')
    if not unit or not cmd:
        return jsonify({"status": "error", "message": "Missing unit or command"}), 400
    
    log_queue.put(f"[MASTER -> {unit}] 하달됨: {cmd}")
    
    def run_unit():
        try:
            # First try in JAM specific folders
            unit_path = os.path.join(TARGET_DIR, "Empire", "JAM_Auto_Forge", unit)
            if not os.path.exists(unit_path):
                unit_path = os.path.join(TARGET_DIR, unit)
            
            p = subprocess.Popen(['python', unit_path, cmd], 
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
            for line in iter(p.stdout.readline, ''):
                if line:
                    log_queue.put(f"[{unit}] {line.strip()}")
            p.stdout.close()
        except Exception as e:
            log_queue.put(f"[{unit}] ERROR: {str(e)}")

    threading.Thread(target=run_unit, daemon=True).start()
    return jsonify({"status": "ok"})

@master_bp.route('/api/master/logs')
def get_logs():
    logs = []
    while not log_queue.empty():
        logs.append(log_queue.get())
    return jsonify({"logs": logs})

@master_bp.route('/api/master/tree')
def get_tree():
    return jsonify({"tree": get_colored_tree(TARGET_DIR)})
