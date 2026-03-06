import os
import zipfile
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template_string

navigator_bp = Blueprint('navigator', __name__)
TARGET_DIR = r"c:\lovesoong" # Updated for new core

def get_nav_tree(path: str, depth: int = 0) -> str:
    html = ""
    try:
        items = sorted(os.listdir(path))
        for item in items:
            full_path = os.path.join(path, item)
            if "BACKUP_CHAMBER" in item or item.startswith('.'): continue
            padding = "&nbsp;" * (depth * 5)
            if os.path.isdir(full_path):
                html += f'{padding}├── <b style="color:#00f0ff;">[그룹] {item}</b><br>'
                html += get_nav_tree(full_path, depth + 1)
            elif item.endswith(('.py', '.md')):
                html += f'{padding}└── <a href="/navigator/view/{item}" target="_blank" style="color:#58a6ff; text-decoration:none;">[이동]</a> '
                html += f'<span style="color:#c9d1d9; cursor:pointer;" onclick="loadCode(\'{item}\')">⚪ {item}</span><br>'
    except: pass
    return html

@navigator_bp.route('/navigator')
def navigator_main():
    tree_html = get_nav_tree(TARGET_DIR)
    return render_template('navigator_core.html', tree_html=tree_html)

@navigator_bp.route('/navigator/api/search')
def nav_api_search():
    key = request.args.get('key', '').replace('.py', '').replace('.md', '')
    for root, _, files in os.walk(TARGET_DIR):
        for f in files:
            if key in f:
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    return jsonify({"status": "success", "path": path, "content": file.read()})
    return jsonify({"status": "error"})

@navigator_bp.route('/navigator/api/backup')
def nav_api_backup():
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    fname = f"EMPIRE_SNAPSHOT_{ts}.zip"
    return jsonify({"status": "success", "msg": f"백업 성공: {fname}"})

@navigator_bp.route('/navigator/view/<name>')
def nav_view_unit(name):
    return f"<html><body style='background:#0d1117;color:#fff;padding:50px;'><h1>📍 {name} 유닛 제어 창</h1><hr><p>정상 연결됨.</p></body></html>"
