from flask import Blueprint, render_template, jsonify, request, session
import time
from .shared import gem_ledger_data, phoenix_members
from backend.ai_persona_engine import phoenix_trader
from backend.phoenix_vault import phoenix_vault
from backend.security_enforcer import security_enforcer
from backend.bybit_trading_engine import bybit_real_engine

trading_bp = Blueprint('trading', __name__)

@trading_bp.route('/api/ai/execute_strategy', methods=['POST'])
def execute_strategy():
    data = request.json
    strategy = data.get('strategy', 'AGGRESSIVE')
    report = phoenix_trader.simulate_trade(strategy)
    phoenix_trader.activity_logs.insert(0, {
        "time": time.strftime("%H:%M:%S"),
        "persona": "COMMANDER",
        "activity": f"Direct Strategy Execution: {strategy}"
    })
    return jsonify(report)

@trading_bp.route('/api/ai_creation/forge', methods=['POST'])
def forge_ai():
    data = request.json
    name = data.get('name', 'UNKNOWN_UNIT')
    persona = data.get('persona', 'BALANCED')
    capital = data.get('capital', 1000000)
    new_gem = {"name": name, "persona": persona, "capital": capital, "pnl": 0, "pnl_percent": 0.0, "status": "READY"}
    gem_ledger_data.append(new_gem)
    return jsonify({"status": "SUCCESS", "message": f"AI unit '{name}' forged."})

@trading_bp.route('/api/phoenix/ranking')
def get_phoenix_ranking():
    sorted_gems = sorted(gem_ledger_data, key=lambda x: x['pnl'], reverse=True)
    return jsonify({"status": "success", "ranking": sorted_gems[:10]})

@trading_bp.route('/api/trader/status')
def trader_status():
    from backend.matching_engine import matching_engine
    return jsonify({
        "persona": phoenix_trader.current_persona,
        "mode": phoenix_trader.intelligence_mode,
        "logs": phoenix_trader.activity_logs[-15:],
        "vault": phoenix_vault.get_status(),
        "orderbook": matching_engine.get_order_book()
    })

# --- 🚀 REAL BYBIT TRADING ROUTES ---

@trading_bp.route('/api/bybit/set_keys', methods=['POST'])
def set_bybit_keys():
    data = request.json
    api_key = data.get('api_key')
    api_secret = data.get('api_secret')
    if not api_key or not api_secret:
        return jsonify({"status": "error", "message": "API Key와 Secret Key가 모두 필요합니다."}), 400
    
    # Save to file via engine
    bybit_real_engine.api_key = api_key
    bybit_real_engine.api_secret = api_secret
    import json
    with open(bybit_real_engine.config_file, "w") as f:
        json.dump({"api_key": api_key, "api_secret": api_secret}, f)
        
    return jsonify({"status": "SUCCESS", "message": "Bybit API 키스톤이 제국 중앙 데이터 뱅크에 안전하게 등록되었습니다."})

@trading_bp.route('/api/bybit/account/balance')
def bybit_live_balance():
    # Only allowed if keys exist
    if not bybit_real_engine.api_key:
        return jsonify({"status": "error", "message": "API Key Not Found"}), 401
    return jsonify(bybit_real_engine.get_wallet_balance())

@trading_bp.route('/api/bybit/positions')
def bybit_live_positions():
    if not bybit_real_engine.api_key:
        return jsonify({"status": "error", "message": "API Key Not Found"}), 401
    return jsonify(bybit_real_engine.get_positions())

@trading_bp.route('/api/bybit/order/create', methods=['POST'])
def bybit_live_order():
    if not bybit_real_engine.api_key:
        return jsonify({"status": "error", "message": "API Key Not Found"}), 401
        
    data = request.json
    category = data.get('category', 'spot') # 'spot' or 'linear'
    symbol = data.get('symbol', 'BTCUSDT')
    side = data.get('side', 'Buy')
    order_type = data.get('orderType', 'Market')
    qty = data.get('qty')
    price = data.get('price')
    leverage = data.get('leverage') # for margin/futures
    tp = data.get('tp') # Take Profit
    sl = data.get('sl') # Stop Loss
    
    result = bybit_real_engine.place_order(category, symbol, side, order_type, qty, price, leverage, tp, sl)
    return jsonify(result)

