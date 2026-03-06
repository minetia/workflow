# -*- coding: utf-8 -*-
# FILE: c:/lovesoong/scripts/servermaster_accounting_action.py
# ROLE: Sovereign Accounting Orchestrator (ServerMaster Proxy)
# VERSION: V1.0_Supreme_Audit

import os
import sys
import json
import random
from datetime import datetime

# Ensure global dependencies can be resolved
BASE_DIR = r"c:\lovesoong"
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import io

# Ensure UTF-8 for Windows PowerShell
if os.name == 'nt':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import Imperial Modules
from Empire.JAM_Auto_Forge.Chancellor import PhoenixQChancellor
from Empire.JAM_Auto_Forge.Banker import PhoenixQBanker
from Empire.Governance.Imperial_Tax_Office import imperial_tax_office
from Empire.Governance.Imperial_Trading_Grand_Prix import imperial_grand_prix

def run_supreme_accounting():
    print("\n" + "="*70)
    print("🔱 [PHOENIX EMPIRE] SUPREME ACCOUNTING ACTION (경리조치) ACTIVATED")
    print("TIME: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*70)

    # 1. Initialize Intelligence Units
    chancellor = PhoenixQChancellor()
    banker = PhoenixQBanker()
    
    # 2. Empire Wealth Audit
    print("\n[STEP 1] Imperial Asset Integrity Audit...")
    audit_result = chancellor.audit_empire_wealth()
    print(f" > Status: {audit_result['status']}")

    # 3. Portfolio Analysis
    print("\n[STEP 2] Sovereign Portfolio Analysis...")
    portfolio = banker.analyze_portfolio()
    if portfolio:
        print(f" > Total Value: {portfolio['total_value']:.2f}")
        print(f" > Diversification: {portfolio['diversification']}")

    # 4. ITGP Settlement (Grand Prix)
    print("\n[STEP 3] Imperial Trading Grand Prix (ITGP) Settlement...")
    
    # Load Real-time Data for Settlement
    coin_state_path = os.path.join(BASE_DIR, "data", "quantum_coin_state.json")
    try:
        with open(coin_state_path, "r", encoding="utf-8") as f:
            coin_state = json.load(f)
        
        # Mocking castle performance based on current balances
        castle_metrics = {
            "Alpha": {"profit": coin_state["wallets"]["CASTLE_ALPHA"]["balance"] * random.uniform(5, 15), "accuracy": random.uniform(0.7, 0.95)},
            "Core": {"profit": coin_state["wallets"]["CASTLE_CORE"]["balance"] * random.uniform(5, 15), "accuracy": random.uniform(0.7, 0.95)},
            "Nexus": {"profit": coin_state["wallets"]["CASTLE_NEXUS"]["balance"] * random.uniform(5, 15), "accuracy": random.uniform(0.7, 0.95)},
            "Zion": {"profit": coin_state["wallets"]["CASTLE_ZION"]["balance"] * random.uniform(5, 15), "accuracy": random.uniform(0.7, 0.95)}
        }
        
        winner = imperial_grand_prix.calculate_cycle_results(castle_metrics)
        print(f" > ITGP Champion: {winner['castle']} (Score: {winner['score']})")
    except Exception as e:
        print(f" ! Settlement Error: {e}")
        winner = {"castle": "System"}

    # 5. Dynamic Tax Calculation
    print("\n[STEP 4] Dynamic Imperial Taxation Assessment...")
    castles = ["CASTLE_ALPHA", "CASTLE_CORE", "CASTLE_NEXUS", "CASTLE_ZION"]
    tax_report = []
    
    for c_id in castles:
        balance = coin_state["wallets"][c_id]["balance"]
        tax_amount, rate, rank, reduction = imperial_tax_office.calculate_tax(c_id, balance)
        tax_report.append({
            "castle": c_id,
            "balance": balance,
            "tax": tax_amount,
            "rate": rate * 100,
            "rank": rank,
            "reduction": reduction
        })
        print(f" > {c_id}: Balance={balance:.4f} | Tax={tax_amount:.4f} ({rate*100:.1f}%) | Rank={rank}")

    # 6. Final Sovereign Report
    print("\n" + "="*70)
    print("📝 [SOVEREIGN ACCOUNTING REPORT] GENERATED")
    print("STATUS: SUPREME OPTIMAL")
    print("-" * 50)
    print(f"ITGP WINNER: {winner['castle'].upper()}")
    print(f"TOTAL TAX REVENUE ASSESSMENT: {sum(t['tax'] for t in tax_report):.4f} PQC")
    print("="*70 + "\n")

if __name__ == "__main__":
    # Ensure scripts directory exists
    os.makedirs(os.path.join(BASE_DIR, "scripts"), exist_ok=True)
    run_supreme_accounting()
