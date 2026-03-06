from flask import Flask
import os
from jinja2 import ChoiceLoader, FileSystemLoader

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "PHOENIX_SECRET_V12")

    # 📁 Configure Multi-Directory Template Loader
    app.jinja_loader = ChoiceLoader([
        FileSystemLoader('.'),
        FileSystemLoader('templates'),
        FileSystemLoader('PHOENIX_MASTER'),
        FileSystemLoader('PHOENIX_CIVITAS'),
        FileSystemLoader('DATA_VAULT'),
        FileSystemLoader('QUANTUM_CORE'),
        FileSystemLoader('workflow_gate'),
        FileSystemLoader('STANDALONE')
    ])

    # 🔗 Register Blueprints
    from routes.auth import auth_bp
    from routes.views import views_bp
    from routes.api_admin import admin_bp
    from routes.api_quantum import quantum_bp
    from routes.api_system import system_bp
    from routes.api_trading import trading_bp
    from routes.navigator import navigator_bp
    from routes.civitas import civitas_bp
    from routes.master_core import master_bp
    from routes.api_sentinel import sentinel_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(quantum_bp)
    app.register_blueprint(system_bp)
    app.register_blueprint(trading_bp)
    app.register_blueprint(navigator_bp)
    app.register_blueprint(civitas_bp)
    app.register_blueprint(master_bp)
    app.register_blueprint(sentinel_bp)

    # 🛡️ Global Security Middleware
    from backend.security_enforcer import security_enforcer
    @app.before_request
    def enforce_security():
        return security_enforcer.enforce_login_logic()

    return app
