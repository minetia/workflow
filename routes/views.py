from flask import Blueprint, render_template, session, jsonify, redirect, url_for
import time, math, os
from .shared import gem_ledger_data, phoenix_members

views_bp = Blueprint('views', __name__)

@views_bp.route('/hq')
def home(): 
    return render_template('ai_architect.html', active_tab='hq')

@views_bp.route('/gateway')
def login_gate_v2(): 
    return render_template('gateway.html')

@views_bp.route('/ledger')
def ledger_view():
    return render_template('master_ledger.html', ledger_data=gem_ledger_data)

@views_bp.route('/vault')
def dual_vault():
    return render_template('dual_vault_system.html', active_tab='vault')

@views_bp.route('/distribution')
def distribution_center():
    return render_template('2_wealth_distribution.html')

@views_bp.route('/member_list')
def member_view():
    return render_template('member_list.html', members=phoenix_members)

@views_bp.route('/analytics')
def analytics_hub():
    return render_template('5_global_analytics.html')

@views_bp.route('/monitor')
def system_monitor():
    return render_template('system_monitor.html')

@views_bp.route('/shield')
def security_shield():
    return render_template('3_risk_management.html', active_tab='shield')

@views_bp.route('/executor')
def global_executor():
    return render_template('5_global_analytics.html', active_tab='executor')

@views_bp.route('/forum')
def public_forum():
    return render_template('forum_board.html')

@views_bp.route('/community')
def public_community():
    return render_template('4_social_community.html', active_tab='community')

@views_bp.route('/tree')
def imperial_tree():
    return render_template('imperial_tree.html', active_tab='hq')

@views_bp.route('/intro')
def imperial_intro():
    if not session.get('authenticated') or session.get('role') not in ['phoenix', 'master']:
        return redirect(url_for('auth.login_gate'))
    return render_template('imperial_intro.html', active_tab='hq')

@views_bp.route('/security_breach')
def security_breach():
    return render_template('security_error.html'), 403

@views_bp.route('/qr')
def qr_entrance():
    return render_template('qr_entrance.html')

@views_bp.route('/architect')
def architect_view(): return render_template('ai_architect.html', active_tab='architect')

@views_bp.route('/risk')
@views_bp.route('/security')
def security_view(): return render_template('3_risk_management.html', active_tab='shield')

@views_bp.route('/global')
@views_bp.route('/tower')
@views_bp.route('/executor_tower')
def executor_tower(): return render_template('5_global_analytics.html', active_tab='executor')

@views_bp.route('/master_control')
@views_bp.route('/strategic_dashboard')
@views_bp.route('/trading_permit')
def strategic_dashboard():
    try:
        from backend.phoenix_vault import phoenix_vault
        from backend.quantum_coin_engine import pqc_engine

        vault_data = phoenix_vault.get_status()
        mining_data = pqc_engine.mining.get_stats()

        total_asset = vault_data.get("total_assets", 10000000)
        tax = vault_data.get("tax_collected", 0)
        pqc_price = mining_data.get("pqc_price", 0)
        pqc_circulating = mining_data.get("circulating", 0)
        pqc_total_mined_today = mining_data.get("total_today", 0)
        vault_v = phoenix_vault.virtual_vault
        vault_r = phoenix_vault.real_vault
        initial = phoenix_vault.initial_capital
        pnl_raw = total_asset - initial
        profit_pct = (pnl_raw / initial * 100) if initial else 0

        stats = {
            "total_asset": f"{total_asset:,.0f}",
            "profit_pct": f"+{profit_pct:.4f}%" if profit_pct >= 0 else f"{profit_pct:.4f}%",
            "tax": f"{tax:,.0f}",
            "virtual_vault": f"{vault_v:,.0f}",
            "real_vault": f"{vault_r:,.0f}",
            "pnl_raw": pnl_raw,
            "pqc_price": pqc_price,
            "pqc_circulating": pqc_circulating,
            "pqc_today": pqc_total_mined_today,
        }
    except:
        stats = {
            "total_asset": "10,000,000", 
            "profit_pct": "+0.0000%",
            "tax": "0",
            "virtual_vault": "0",
            "real_vault": "0",
            "pnl_raw": 0,
            "pqc_price": 0,
            "pqc_circulating": 0,
            "pqc_today": 0,
        }
    
    return render_template('strategic_dashboard.html', active_tab='strategic', stats=stats)

@views_bp.route('/u/dashboard')
@views_bp.route('/dashboard')
def user_dashboard(): return render_template('user_dashboard.html', active_tab='dashboard')

@views_bp.route('/hub')
def commander_hub():
    return render_template('analytics_hub.html', active_tab='hub')

@views_bp.route('/server')
def server_master(): return render_template('system_monitor.html')

@views_bp.route('/command')
def command_center(): return render_template('admin_dashboard.html', active_tab='command')

@views_bp.route('/quantum_singularity')
def quantum_singularity():
    return render_template('quantum_singularity.html')

@views_bp.route('/judiciary')
def supreme_court():
    return render_template('judiciary.html')

@views_bp.route('/dungeon')
def dungeon():
    return render_template('dungeon.html')

@views_bp.route('/map')
def imperial_map():
    return render_template('imperial_map.html', page_title='IMPERIAL MAP')

@views_bp.route('/colosseum')
def colosseum():
    return render_template('colosseum.html')

@views_bp.route('/vault_analytics')
def vault_analytics():
    return render_template('vault_analytics.html')

@views_bp.route('/api_monitor')
def api_monitor():
    return render_template('api_monitor.html')

@views_bp.route('/backup_chamber')
def backup_chamber():
    return render_template('backup_chamber.html')

@views_bp.route('/incinerator')
def incinerator():
    return render_template('incinerator.html')

@views_bp.route('/quantum_telemetry')
def quantum_telemetry():
    return render_template('quantum_telemetry.html')

@views_bp.route('/sentinel')
def sentinel_monitor():
    return render_template('sentinel_dashboard.html')
@views_bp.route('/hub_center')
def hub_center():
    return render_template('analytics_hub.html')

@views_bp.route('/network_trace')
def network_trace():
    return render_template('api_monitor.html')



@views_bp.route('/trading_4d')
def trading_4d():
    return render_template('bybit_live.html')

@views_bp.route('/market')
def imperial_market():
    return render_template('admin_dashboard.html')

@views_bp.route('/whitepaper')
def whitepaper():
    return render_template('whitepaper_viewer.html')

@views_bp.route('/supreme_tower')
def supreme_tower():
    return render_template('supreme_tower.html')

@views_bp.route('/standalone/<path:filename>')
def serve_standalone(filename):
    if filename.endswith('.html'):
        return render_template(filename)
    from flask import send_from_directory
    import os
    standalone_dir = os.path.join(os.getcwd(), 'STANDALONE')
    return send_from_directory(standalone_dir, filename)

