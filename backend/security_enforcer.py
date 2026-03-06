import json
import os
from datetime import datetime
from flask import request, session, redirect, url_for, render_template
from pathlib import Path

class SecurityEnforcer:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.audit_log_file = self.base_dir / "data" / "audit_log.json"
        self._ensure_audit_log()

    def _ensure_audit_log(self):
        if not self.audit_log_file.parent.exists():
            os.makedirs(self.audit_log_file.parent)
        if not self.audit_log_file.exists():
            with open(self.audit_log_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def log_action(self, user_role, action, details):
        """본부급 행위 감사 로그 기록"""
        if not user_role or user_role not in ['phoenix', 'admin']:
            return

        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "role": user_role,
            "action": action,
            "details": details,
            "ip": request.remote_addr
        }

        try:
            with open(self.audit_log_file, "r+", encoding="utf-8") as f:
                logs = json.load(f)
                logs.append(log_entry)
                f.seek(0)
                json.dump(logs[-1000:], f, indent=2, ensure_ascii=False) # 최근 1000개 유지
        except Exception as e:
            print(f"[AUDIT LOG ERROR] {e}")

    def check_ip_pinning(self, user_role):
        """[피닉스] 세션 IP 고정 체크"""
        if user_role != 'phoenix':
            return True

        current_ip = request.remote_addr
        pinned_ip = session.get('pinned_ip')

        if not pinned_ip:
            session['pinned_ip'] = current_ip
            return True
        
        if pinned_ip != current_ip:
            print(f"[SECURITY ALERT] Master Session Hijacking Attempt! Expected {pinned_ip}, got {current_ip}")
            # 🔱 [INCARCERATION]
            try:
                from Empire.Governance.Imperial_Quantum_Dungeon import imperial_dungeon
                imperial_dungeon.incarcerate(current_ip, f"Session Hijacking Attempt targeting Phoenix Role", severity="CRITICAL")
            except Exception as e:
                print(f"[DUNGEON ERROR] Failed to incarcerate: {e}")
            
            session.clear()
            return False
        
        return True

    def get_required_level(self, path):
        """특정 경로에 대한 요구 권한 레벨을 반환합니다."""
        from routes.shared import ZONE_PERMISSIONS, ACCESS_LEVELS
        for prefix, req in ZONE_PERMISSIONS.items():
            if path.startswith(prefix):
                return ACCESS_LEVELS[req] if isinstance(req, str) else req
        return 0

    def enforce_login_logic(self):
        """Flask before_request용 로그인 강제 로직"""
        from routes.shared import ACCESS_LEVELS
        
        # 로클 접속(사령관님)은 모든 보안 검사 패스
        trusted_ips = ['127.0.0.1', '::1']
        is_local = request.remote_addr in trusted_ips
        
        if is_local:
            session['authenticated'] = True
            session['role'] = 'phoenix'
            session['imperial_auth'] = True
            return

        exempt_paths = [
            '/', '/ai_login', '/ai_signup', '/security_breach', 
            '/api/auth/status', '/api/auth/send_telegram', 
            '/api/auth/verify_telegram', '/api/auth/user_login',
            '/api/auth/verify', '/jam/commander_center', '/jam/gemini2'
        ]
        
        if 'antigravity/brain' in request.path or '/static/' in request.path:
            return
            
        # [PHOENIX-STEALTH] 제국 기밀 유지 인증 체크
        if not session.get('imperial_auth'):
            # 인증 게이트 및 필수 정적 리소스는 예외
            stealth_exempt = ['/imperial_auth', '/maintenance', '/static/']
            if not any(request.path.startswith(p) for p in stealth_exempt):
                return render_template('maintenance.html'), 403

        is_authenticated = session.get('authenticated', False)
        user_role = session.get('role', None)
        
        if request.path not in exempt_paths and not is_authenticated:
            if '.' not in request.path or request.path.endswith('.html'):
                return redirect(url_for('auth.login_gate'))

        if is_authenticated:
            session.permanent = True
            if not self.check_ip_pinning(user_role):
                return redirect(url_for('auth.login_gate'))
                
            if user_role == 'phoenix':
                return
                
            required_level = self.get_required_level(request.path)
            if required_level > 0:
                current_level = ACCESS_LEVELS.get(user_role, 0)
                if current_level < required_level:
                    return redirect(url_for('views.security_breach'))

    def mask_data(self, data, user_role, min_level=4):
        """[PHOENIX-V12] 권한 기반 데이터 마스킹 - 민감 정보 보호"""
        from routes.shared import ACCESS_LEVELS
        
        # 권한 레벨 확인
        user_level = ACCESS_LEVELS.get(user_role, 0)
        
        # 충분한 권한이 있거나 데이터가 짧으면 원본 반환
        if user_level >= min_level or not data:
            return data
            
        # 🛡️ 마스킹 처리 (중간 8자리를 *로 대체하여 보안 유지)
        if len(data) > 12:
            return f"{data[:6]}********{data[-4:]}"
        elif len(data) > 4:
            return f"{data[:2]}****{data[-2:]}"
        return "********"

security_enforcer = SecurityEnforcer()
