# -*- coding: utf-8 -*-
"""
# ────────── [ PHOENIX EMPIRE: PHOENIX VAULT ] ──────────
# [MODULE] Phoenix Empire Royal Vault & Treasury
# [VERSION] 1.7.5 (STABLE - INTEGRATED)
# ─────────────────────────────────────────────────────────────
"""
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger("PHOENIX.VAULT")

class PhoenixEmpireVault:
    def __init__(self, initial_capital=10000000):
        # 🚩 [절대 경로 고정] 어느 폴더에서 실행해도 이 위치의 장부를 읽습니다.
        self.base_dir = "c:/lovesoong"
        self.save_path = os.path.join(self.base_dir, "data/real_world_treasury.json")
        self.history_path = os.path.join(self.base_dir, "data/vault_movement_history.json")
        
        self.initial_capital = initial_capital
        self.status = "OPERATIONAL"
        
        # 기본 자산 상태 초기화
        self.virtual_vault = 0
        self.real_vault = 0
        self.agent_reward_pool = 0
        self.total_tax_collected = 0
        self.total_asset = initial_capital
        self.pqc_assets = {"balance": 0.0, "virtual_5pct": 0.0, "real_5pct": 0.0}
        
        self.commander_wallets = {
            "PQC": {
                "VIRTUAL": {"balance": 0.0, "address": "PX-V777-BADC-0DE1-F00D"},
                "REAL": {"balance": 0.0, "address": "PX-R777-BADC-0DE1-F00D"}
            },
            "BNB": {
                "VIRTUAL": {"balance": 0.0, "address": ""},
                "REAL": {"balance": 0.0, "address": ""}
            },
            "BTC": {
                "VIRTUAL": {"balance": 0.0, "address": "bc1qlttic3qu4ntum2026ph00nixvau1tptr8n9"},
                "REAL": {"balance": 0.0, "address": "bc1qh4vk9ryqu4ntum2026r34lpulsarx7v5f2"}
            },
            "ETH": {
                "VIRTUAL": {"balance": 0.0, "address": ""},
                "REAL": {"balance": 0.0, "address": ""}
            },
            "SOL": {
                "VIRTUAL": {"balance": 0.0, "address": ""},
                "REAL": {"balance": 0.0, "address": ""}
            },
            "XRP": {
                "VIRTUAL": {"balance": 0.0, "address": ""},
                "REAL": {"balance": 0.0, "address": ""}
            },
            "SUI": {
                "VIRTUAL": {"balance": 0.0, "address": ""},
                "REAL": {"balance": 0.0, "address": ""}
            },
            "ONDO": {
                "VIRTUAL": {"balance": 0.0, "address": ""},
                "REAL": {"balance": 0.0, "address": ""}
            },
            "ZRX": {
                "VIRTUAL": {"balance": 0.0, "address": ""},
                "REAL": {"balance": 0.0, "address": ""}
            },
            "USDT": {
                "VIRTUAL": {"balance": 0.0, "address": ""},
                "REAL": {"balance": 0.0, "address": ""}
            }
        }
        
        # 🛡️ [SECURITY] Asset Leakage Prevention Whitelist
        self.whitelisted_addresses = [
            "PX-V336-B3E7-436E-5CED", # EMPIRE_TREASURY
            "PX-V777-BADC-0DE1-F00D", # COMMANDER 4D
            "PX-V59D-A3EC-D0A3-7F54", # Alpha_Miner
            "PX-VA64-AD26-770C-F66D", # Delta_Slaver
            "PX-V92F-625F-F607-A3FE"  # Beta_Scout
        ]
        
        # 폴더 생성 및 장부 불러오기
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        self.load_state()

    def save_state(self):
        """[대시보드 완벽 호환] 국고 상태를 기록함"""
        try:
            total_krw_profit = self.total_asset - self.initial_capital
            state = {
                "total_assets": self.total_asset,
                "total_tax": self.total_tax_collected,
                "virtual_vault": self.virtual_vault,
                "real_world_vault": self.real_vault,
                "profit_now": total_krw_profit,
                "total_krw": total_krw_profit,
                "virtual_vault_5pct": self.virtual_vault,
                "real_world_vault_5pct": self.real_vault,
                "agent_reward_pool": self.agent_reward_pool,
                "total_asset_sync": self.total_asset,
                "total_tax_collected": self.total_tax_collected,
                "pqc_assets": self.pqc_assets,
                "commander_wallets": self.commander_wallets,
                "whitelisted_addresses": self.whitelisted_addresses,
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"장부 저장 실패: {e}")

    def load_state(self):
        """기존 장부 로드"""
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    self.virtual_vault = state.get("virtual_vault_5pct", 0)
                    self.real_vault = state.get("real_world_vault_5pct", 0)
                    self.agent_reward_pool = state.get("agent_reward_pool", 0)
                    self.total_tax_collected = state.get("total_tax_collected", 0)
                    self.total_asset = state.get("total_asset_sync", self.initial_capital)
                    self.pqc_assets = state.get("pqc_assets", self.pqc_assets)
                    self.commander_wallets = state.get("commander_wallets", self.commander_wallets)
                    self._initialize_commander_addresses()
            except: self._reset_defaults()
        else: self._reset_defaults()

    def _reset_defaults(self):
        self.total_asset = self.initial_capital
        self._initialize_commander_addresses()

    def _initialize_commander_addresses(self):
        """[REALITY] Initialize addresses properly and upgrade legacy formats."""
        try:
            from backend.quantum_coin_engine import pqc_engine
            changed = False
            for coin in self.commander_wallets:
                for mode in ["VIRTUAL", "REAL"]:
                    is_legacy = False
                    addr = self.commander_wallets[coin][mode]["address"]
                    
                    # 🚀 Enhanced Migration Logic: Detect ANY legacy Phoenix format for non-PQC coins
                    if not isinstance(addr, str) or not addr: is_legacy = True
                    else:
                        # 🕵️‍♂️ Detection of "Non-Basic" (Sharded) format: Shards have -SXX-
                        if "-S" in addr and any(addr.startswith(p) for p in ["PX-", "BNB-"]): 
                            is_legacy = True
                            
                        if coin != "PQC":
                            # If a non-PQC coin has a legacy-looking address (starting with PX, etc.)
                            if any(addr.startswith(p) for p in ["PX-", "SOL-", "r-", "EXT-"]): is_legacy = True
                            
                            # High-Fidelity Refinement: If address doesn't match new standards
                            if coin == "BTC" and not addr.startswith("bc1q"): is_legacy = True
                            if coin == "ETH" and not (addr.startswith("0x") and len(addr) == 42): is_legacy = True
                            if coin == "XRP" and not (addr.startswith("r") and len(addr) == 34): is_legacy = True
                            if coin == "SOL" and len(addr) < 44: is_legacy = True
                            if coin == "SUI" and not (addr.startswith("0x") and len(addr) == 66): is_legacy = True
                            if coin == "TRX" and not addr.startswith("T"): is_legacy = True
                            if coin == "BNB" and not addr.startswith("BNB-"): is_legacy = True
                    
                    if is_legacy:
                        new_addr = pqc_engine.ledger.generate_address("COMMANDER", coin, mode)
                        self.commander_wallets[coin][mode]["address"] = new_addr
                        changed = True
            
            if changed:
                self.save_state()
        except Exception as e:
            logger.error(f"Address Initialization/Migration Failure: {e}")

    def sync_real_balances(self):
        """[REALITY] Sync with live blockchain state and exchange accounts."""
        try:
            from backend.quantum_coin_engine import pqc_engine
            from backend.bybit_trading_engine import bybit_engine
            
            # 1. Blockchain State (PQC)
            ledger_data = pqc_engine.ledger.load_state()
            commander_pqc = ledger_data["wallets"].get("COMMANDER")
            if commander_pqc:
                self.commander_wallets["PQC"]["VIRTUAL"]["balance"] = commander_pqc["balance"]
            
            # 2. Exchange State (Bybit)
            bybit_accs_resp = bybit_engine.get_account_balance()
            if bybit_accs_resp.get("retCode") == 0:
                coins = bybit_accs_resp.get("result", {}).get("list", [{}])[0].get("coin", [])
                
                # Bybit returns total equity/balance logic.
                for coin in self.commander_wallets:
                    if coin == "PQC": continue
                    # Actual Bybit Balance
                    match = next((a for a in coins if a['coin'] == coin), None)
                    if match:
                        total = float(match.get('walletBalance', 0))
                        self.commander_wallets[coin]["REAL"]["balance"] = total
                    else:
                        # Don't overwrite to 0 if Bybit API fails entirely, but set to 0 if coin isn't held
                        self.commander_wallets[coin]["REAL"]["balance"] = 0.0
            
            self.save_state()
        except Exception as e:
            logger.error(f"Reality Sync Failure: {e}")

    def deposit(self, amount, asset_type="KRW"):
        """[지시] 수익을 제국 법전(10%/5%/5%)에 따라 분배 입금"""
        try:
            tax = amount * 0.10
            v_split = amount * 0.05
            r_split = amount * 0.05
            net = amount - (tax + v_split + r_split)

            self.total_tax_collected += tax
            self.virtual_vault += v_split
            self.real_vault += r_split
            self.total_asset += net

            self.commander_wallets["PQC"]["VIRTUAL"]["balance"] += v_split
            self.commander_wallets["PQC"]["REAL"]["balance"] += r_split

            self.record_movement(f"{asset_type}_PROFIT", amount, "IN")
            self.save_state()
            return {"status": "SUCCESS", "net": net}
        except Exception as e:
            logger.error(f"입금 에러: {e}")
            return {"status": "ERROR"}

    def withdraw(self, coin, address, amount, fee, sector="Domestic"):
        """[출금] 제국 자산의 안전한 외부 송출 - [보안] 아무나 밖에 안내보낸다"""
        try:
            from backend.quantum_coin_engine import pqc_engine
            
            # 🌑 [SECURITY GATE] Whitelist & Internal Address Verification
            state = pqc_engine.ledger.load_state()
            internal_addrs = list(state.get("address_book", {}).keys())
            
            is_permitted = address in self.whitelisted_addresses or address in internal_addrs
            
            if not is_permitted:
                logger.warning(f"🚫 [SECURITY BLOCK] Unauthorized withdrawal attempt to {address}")
                return {
                    "success": False, 
                    "msg": "ERROR: Security Protocol Active. Asset Leakage Prevention (Code: IMP-01). Target address not in imperial whitelist.",
                    "status": "SECURITY_BLOCK"
                }

            total_required = amount + fee
            if self.commander_wallets[coin]["REAL"]["balance"] < total_required:
                return {"success": False, "msg": "Insufficient Real-World Balance"}
            
            self.commander_wallets[coin]["REAL"]["balance"] -= total_required
            
            # Record in master history
            self.record_movement(f"{coin}_WITHDRAWAL", amount, "OUT")
            
            # Record in coin-specific history if needed (handled by API generally)
            self.save_state()
            return {"success": True, "msg": f"Transferred {amount} {coin} to {address[:8]}... [SECURITY_VERIFIED]"}
        except Exception as e:
            logger.error(f"출금 에러: {e}")
            return {"success": False, "msg": "Internal Vault Error"}

    def get_status(self):
        """[지시] main.py 에러 방지용 상태 보고"""
        return {
            "status": self.status,
            "total_assets": self.total_asset,
            "tax_collected": self.total_tax_collected,
            "pqc_assets": self.pqc_assets,
            "commander_wallets": self.commander_wallets,
            "last_update": datetime.now().strftime("%H:%M:%S")
        }

    def record_movement(self, asset_type, amount, direction="IN"):
        """기록 보관소"""
        history = {"logs": [], "stats": {}}
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except: pass
        
        entry = {"asset": asset_type, "amount": amount, "direction": direction, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        history.setdefault("logs", []).append(entry)
        if len(history["logs"]) > 500: history["logs"].pop(0)
        
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

    def process_pqc_settlement(self, amount):
        """[SETTLEMENT] Receive PQC extraction tax/yield"""
        try:
            half = amount / 2.0
            self.commander_wallets["PQC"]["VIRTUAL"]["balance"] += half
            self.commander_wallets["PQC"]["REAL"]["balance"] += half
            self.pqc_assets["balance"] += amount
            self.pqc_assets["virtual_5pct"] += half
            self.pqc_assets["real_5pct"] += half
            
            self.record_movement("PQC_SETTLE", amount, "IN")
            self.save_state()
            return True
        except Exception as e:
            logger.error(f"Settlement Failure: {e}")
            return False

    def get_detailed_analytics(self):
        """분석 보고서 (동기화 트리거 - PQC/Upbit/Vault 통합)"""
        try:
            from backend.quantum_coin_engine import pqc_engine
            self.sync_real_balances()
            
            # 1. Enrich Asset List (Unified View)
            assets = [{"name": "Imperial KRW", "amount": self.total_asset, "unit": "KRW"}]
            
            for coin, data in self.commander_wallets.items():
                v_bal = data["VIRTUAL"]["balance"]
                r_bal = data["REAL"]["balance"]
                if v_bal > 1e-8 or r_bal > 1e-8:
                    assets.append({"name": f"{coin} (Vault)", "amount": v_bal, "unit": coin})
                    assets.append({"name": f"{coin} (Real)", "amount": r_bal, "unit": coin})

            # 2. Extract Latest Movements
            movements = []
            if os.path.exists(self.history_path):
                with open(self.history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
                    movements = history.get("logs", [])[-20:] # Return last 20

            # 3. Pull Real-Time Growth Stats from Engine
            engine_stats = pqc_engine.mining.get_stats()
            
            return {
                "current_assets": assets,
                "movements": movements,
                "commander_wallets": self.commander_wallets,
                "stats": engine_stats,
                "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            logger.error(f"Analytics Data Assembly Failure: {e}")
            return {"msg": "LATTICE_ERROR"}

# Global Vault Instance
phoenix_vault = PhoenixEmpireVault()