from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import random
import string
import urllib.request
import urllib.parse
import json
from .shared import auth_state
from backend.security_enforcer import security_enforcer

auth_bp = Blueprint('auth', __name__)

# 🤖 제국 텔레그램 봇 설정 (실제 토큰 기입 필요)
TELEGRAM_BOT_TOKEN = "8586852392:AAGiyKVi2CNQTT4eRlUVcESW8GBQgl6v_WA"
TELEGRAM_CHAT_ID = "1107103330"

@auth_bp.route('/')
def login_gate(): 
    session.clear() # Reset on load
    return render_template('login.html')

@auth_bp.route('/ai_login')
def ai_login(): return render_template('login.html')

@auth_bp.route('/ai_signup')
def ai_signup(): return render_template('ai_register.html')

@auth_bp.route('/api/auth/status')
def auth_status():
    return jsonify({
        "verified": session.get('authenticated', False),
        "role": session.get('role', None)
    })

@auth_bp.route('/api/auth/verify_telegram', methods=['POST'])
def verify_telegram_code():
    data = request.json
    submitted_code = data.get("code", "").upper()
    
    if "telegram_code" in auth_state and auth_state["telegram_code"] and submitted_code == auth_state["telegram_code"]:
        session['authenticated'] = True
        session['role'] = 'master'
        return jsonify({"status": "success", "redirect": "/jam/nexus"})
    else:
        return jsonify({"status": "error", "message": "텔레그램 보안 코드가 일치하지 않습니다."}), 401

@auth_bp.route('/api/auth/verify', methods=['POST'])
def verify_login():
    data = request.json
    submitted_id = data.get("id")
    submitted_code = data.get("code")
    
    is_master = False
    if submitted_code == "8282":
        is_master = True
    elif "telegram_code" in auth_state and auth_state["telegram_code"] and submitted_code == auth_state["telegram_code"]:
        is_master = True

    if is_master:
        session['authenticated'] = True
        session['role'] = 'phoenix'
        return jsonify({"status": "success", "redirect": "/jam/nexus"})

    if submitted_id and submitted_code:
        session['authenticated'] = True
        session['role'] = 'user'
        session['user_id'] = submitted_id
        return jsonify({"status": "success", "redirect": "/gateway"})

    return jsonify({"status": "error", "message": "비밀번호 또는 보안 코드가 올바르지 않습니다."}), 401

@auth_bp.route('/api/auth/user_login', methods=['POST'])
def user_login():
    data = request.json
    user_id = data.get("id")
    password = data.get("password")
    
    if user_id and password:
        session['authenticated'] = True
        session['role'] = 'user'
        session['user_id'] = user_id
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "아이디와 비밀번호를 입력해주세요."}), 401

@auth_bp.route('/api/auth/user_signup', methods=['POST'])
def user_signup():
    data = request.json
    user_id = data.get("id")
    password = data.get("password")
    
    if user_id and password:
        return jsonify({"status": "success", "message": "가입 성공"})
    else:
        return jsonify({"status": "error", "message": "필수 정보를 모두 입력해주세요."}), 400

@auth_bp.route('/api/auth/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login_gate'))

@auth_bp.route('/api/auth/send_telegram', methods=['POST'])
def send_telegram():
    chars = string.ascii_uppercase + string.digits + "!@#$%"
    telegram_code = ''.join(random.choices(chars, k=6))
    auth_state['telegram_code'] = telegram_code
    
    base_url = request.host_url.rstrip('/')
    commander_url = f"{base_url}/"
    user_url = f"{base_url}/ai_login"

    message = (
        f"👑 [PHOENIX EMPIRE]\n"
        f"사령관님, 제국 사령부 원격 접속 항로가 개설되었습니다.\n\n"
        f"🔑 특수 보안 코드 (클릭 시 복사):\n`{telegram_code}`\n\n"
        f"📍 [사령관 전용 관리 주소]\n`{commander_url}`\n\n"
        f"📍 [일반 유저 접속 주소]\n`{user_url}`"
    )
    
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID":
        return jsonify({"status": "error", "message": "텔레그램 설정 오류"}), 400

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({'chat_id': TELEGRAM_CHAT_ID, 'text': message}).encode('utf-8')
    try:
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req) as response:
            return jsonify({"status": "SUCCESS", "message": "텔레그램 전송 완료"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
