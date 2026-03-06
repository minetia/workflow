from flask import Blueprint, render_template, jsonify, request, session
from backend.quantum_coin_engine import pqc_engine
from backend.security_enforcer import security_enforcer

civitas_bp = Blueprint('civitas', __name__)

@civitas_bp.route('/civitas')
def civitas_center(): return render_template('PHOENIX_CIVITAS/civitas_center.html')

@civitas_bp.route('/civitas/park')
def civitas_park(): return render_template('PHOENIX_CIVITAS/park.html')

@civitas_bp.route('/api/civitas/purchase', methods=['POST'])
def civitas_purchase():
    data = request.json
    item = data.get('item')
    price = data.get('price')
    role = session.get('role')
    result = pqc_engine.transfer_pqc("PQC_USER", "EMPIRE_TREASURY", price)
    return jsonify(result)
