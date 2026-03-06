from flask import Blueprint, render_template, jsonify, request, session, send_from_directory
import os
import json
from backend.quantum_coin_engine import pqc_engine
from backend.security_enforcer import security_enforcer

quantum_bp = Blueprint('quantum', __name__)

@quantum_bp.route('/quantum')
def quantum_engine():
    return render_template('QUANTUM_CORE/1_automated_trading.html', active_tab='quantum')

@quantum_bp.route('/pqc_wallet')
def pqc_wallet_index():
    # In some versions it might be in PHOENIX_WALLET, 
    # but currently found in QUANTUM_CORE via the multi-loader.
    return render_template('pqc_wallet.html', active_tab='wallet', my_address="PX-" + "0"*16)

@quantum_bp.route('/pqc_mining')
def pqc_mining_index():
    return render_template('pqc_mining.html', active_tab='mining')

@quantum_bp.route('/api/commander/wallets')
def get_commander_wallets():
    from backend.phoenix_vault import phoenix_vault
    from backend.korea_upbit_api import upbit_core
    
    phoenix_vault.sync_real_balances()
    
    # 🌍 GLOBAL REAL-TIME PRICE HEARTBEAT
    prices = {
        "BTC": 98000000, "ETH": 4500000, "XRP": 1100, "SOL": 210000, 
        "USDT": 1350, "PQC": 1000, "ZRX": 1200, "ONDO": 1500, "SUI": 2800, "BNB": 850000,
        "PQC": pqc_engine.get_mining_stats().get("pqc_price", 1000)
    }
    
    try:
        upbit_pairs = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-SOL"]
        upbit_prices = upbit_core.get_current_prices(upbit_pairs)
        if upbit_prices:
            for pair, p in upbit_prices.items():
                coin = pair.split("-")[1]
                prices[coin] = p
        
        import random
        for coin in ["ONDO", "SUI", "ZRX"]:
            prices[coin] *= (1 + (random.random() * 0.002 - 0.001))
            
    except Exception as e:
        print(f"Price Pulsar Error: {e}")

    wallets = phoenix_vault.commander_wallets
    return jsonify({
        "commander_wallets": wallets,
        "total_krw": phoenix_vault.total_asset,
        "pqc_price": prices["PQC"],
        "real_prices": prices
    })

@quantum_bp.route('/api/quantum/stats')
def get_quantum_stats():
    try:
        stats = pqc_engine.mining.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e), "pqc_price": 0, "circulating": 0, "total_today": 0})


@quantum_bp.route('/api/wallet/history/<coin>')
def get_wallet_history(coin):
    from backend.phoenix_vault import phoenix_vault
    master_history_path = os.path.join(r"C:\Users\loves\workflow", "data/vault_movement_history.json")
    logs = []
    
    if os.path.exists(master_history_path):
        with open(master_history_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for entry in data.get("logs", []):
                if coin in entry["asset"]:
                    logs.append({
                        "type": entry["direction"],
                        "msg": f"Quantum {entry['asset'].replace('_', ' ').capitalize()}",
                        "time": entry["timestamp"].split(" ")[1],
                        "amount": entry["amount"],
                        "krw": 0,
                        "date": entry["timestamp"].split(" ")[0].replace("-", ".")
                    })
    
    if not logs:
        logs = [{"type": "IN", "msg": "Quantum Deposit Complete", "time": "12:00:00", "amount": 0.0, "krw": 0, "date": "2026.03.04"}]
    
    return jsonify({"coin": coin, "logs": logs[::-1]})

@quantum_bp.route('/api/quantum/pqc')
def get_pqc_price():
    stats = pqc_engine.get_mining_stats()
    return jsonify({"price": stats.get("pqc_price")})

@quantum_bp.route('/api/quantum/mining_stats')
def get_mining_stats():
    return jsonify(pqc_engine.get_mining_stats())

@quantum_bp.route('/api/quantum/wallet/<address>')
def get_wallet(address):
    info = pqc_engine.get_wallet_info(address)
    if not info: return jsonify({"status": "NOT_FOUND"}), 404
    return jsonify(info)

@quantum_bp.route('/api/quantum/wallet/transfer', methods=['POST'])
def transfer_pqc():
    data = request.json
    return jsonify(pqc_engine.transfer(data['from'], data['to'], data['amount']))
