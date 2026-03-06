from flask import session, redirect, url_for, request, render_template
import functools

# [PHOENIX_MASTER] Stealth Auth System
IMPERIAL_PIN = "7777"

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('imperial_auth'):
            # 비인가 접근 시 위장 페이지(Under Maintenance)로 유도
            return render_template('maintenance.html'), 403
        return f(*args, **kwargs)
    return decorated_function

def check_auth(pin):
    if pin == IMPERIAL_PIN:
        session['imperial_auth'] = True
        session.permanent = True
        return True
    return False

def logout():
    session.pop('imperial_auth', None)
