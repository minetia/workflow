import json
import os
import random
import hashlib
from datetime import datetime

class PQCLedger:
    def __init__(self, engine):
        self.engine = engine
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.state_dir = os.path.join(self.base_dir, "data")
        self.log_dir = os.path.join(self.base_dir, "SYSTEM_LOGS")
        
        self.state_file = os.path.join(self.state_dir, "quantum_coin_state.json")
        self.log_file = os.path.join(self.log_dir, "quantum_coin.log")
        
        self.ensure_files()

    def generate_address(self, seed, coin="PQC", mode="VIRTUAL", shard_id=None, proxy=False, stealth=False):
        # 🕵️‍♂️ Imperial Shadow Policy: Default to standard formats for external coins
        # The internal Phoenix format (PX-) is only for PQC or explicit Proxy modes
        
        # 1. Base realistic hash for external appearance
        hash_obj = hashlib.sha256(f"{seed}_{coin}_{mode}_IMPERIAL".encode()).hexdigest()
        
        # 2. Return standard formats by default for non-PQC coins (unless proxy is requested)
        if not proxy:
            # 🎨 Individualized Coin Protocol (Absolute Fidelity)
            if coin == "BTC": 
                return f"bc1q{hash_obj[:38]}" # Bech32 SegWit
            if coin in ["ETH", "USDT", "ONDO", "ZRX"]: 
                return f"0x{hash_obj[:40]}" # EVM Standard
            if coin == "XRP": 
                # Ripple Base58 r-address emulation
                chars = "rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuv"
                r_body = "".join(chars[int(hash_obj[i:i+2], 16) % len(chars)] for i in range(0, 64, 2))
                return f"r{r_body[:33]}"
            if coin == "SOL": 
                # Solana Base58 emulation (No prefix) - Use SHA512 for longer hash
                h512 = hashlib.sha512(f"{seed}_{coin}_{mode}_IMPERIAL_SOL".encode()).hexdigest()
                chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
                s_body = "".join(chars[int(h512[i:i+2], 16) % len(chars)] for i in range(0, 88, 2))
                return s_body[:44]
            if coin == "SUI":
                return f"0x{hash_obj[:64]}" # Sui 32-byte hex
            if coin == "TRX": 
                return f"T{hash_obj[:33]}" # Tron Mainnet T-address
        
        # 3. Phoenix Internal/Proxy format
        prefix_map = {"PQC": "PX", "BTC": "1", "ETH": "0x", "SOL": "SOL", "XRP": "r", "BNB": "BNB"}
        prefix = prefix_map.get(coin, "PX")
        if proxy: prefix = "PX-PRX" 
            
        mode_id = "V" if mode == "VIRTUAL" else "R"
        hash_val = hashlib.sha256(f"{seed}_{mode}_{coin}_{shard_id}_{proxy}_{stealth}".encode()).hexdigest()
        short_hash = hash_val[:16].upper()
        
        # 🛡️ Dual-Layer Format: Basic (4 blocks) vs Sharded (5 blocks + SXX)
        if shard_id is not None:
            shard_prefix = f"S{shard_id:02d}"
            return f"{prefix}-{shard_prefix}-{mode_id}{short_hash[0:3]}-{short_hash[3:7]}-{short_hash[7:11]}-{short_hash[11:15]}"
        else:
            # 🌑 Basic Phoenix Format (Legacy Compatible)
            return f"{prefix}-{mode_id}{short_hash[0:3]}-{short_hash[3:7]}-{short_hash[7:11]}-{short_hash[11:15]}"

    def ensure_files(self):
        os.makedirs(self.state_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        if not os.path.exists(self.state_file):
            addr = self.generate_address("EMPIRE_TREASURY_SEED_2026")
            initial = {
                "total_supply": 1000000000.0, "circulating_supply": 0.0, "burned_supply": 0.0,
                "network_speed": 1.0, "gold_backed_reserve_kg": 500.0, "rwa_inventory": [],
                "wallets": {"EMPIRE_TREASURY": {"balance": 1000000000.0, "address": addr, "level": 4}},
                "address_book": {addr: "EMPIRE_TREASURY"}, "mining_history": {"by_minute": {}, "total_mined_today": 0.0},
                "transactions": []
            }
            self.save_state(initial)
        else:
            # 🔄 Migration: Ensure all wallets have a level
            data = self.load_state()
            updated = False
            for name, wallet in data.get("wallets", {}).items():
                if "level" not in wallet:
                    wallet["level"] = 1 if name != "EMPIRE_TREASURY" else 4
                    updated = True
            if updated:
                self.save_state(data)

    def load_state(self):
        with open(self.state_file, "r") as f:
            return json.load(f)

    def save_state(self, data):
        data["gold_backed_reserve_kg"] = getattr(self.engine, 'gold_backed_reserve_kg', 500.0)
        data["network_speed"] = getattr(self.engine, 'quantum_speed', 1.0)
        temp_file = self.state_file + ".tmp"
        with open(temp_file, "w") as f:
            json.dump(data, f, indent=4)
        os.replace(temp_file, self.state_file)

    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {msg}\n")

    def get_wallet_info(self, address):
        data = self.load_state()
        name = data["address_book"].get(address)
        if not name: return {"address": address, "balance": 0.0, "status": "NOT_FOUND"}
        wallet = data["wallets"][name]
        history = []
        
        # 🕵️‍♂️ Detection logic for shadow/proxy
        is_shadow = address.startswith("bc1q") or address.startswith("0x") and not any(m in address for m in ["-V", "-R"])
        is_proxy = "PX-PRX" in address
        
        for tx in data.get("transactions", []):
            if tx["from"] == address or tx["to"] == address:
                # Add synthetic routing info
                if is_shadow:
                    tx["routing"] = "Quantum Shadow (External Alias)"
                elif is_proxy:
                    tx["routing"] = "Imperial Proxy (Routed via Global Nexus)"
                else:
                    tx["routing"] = "Direct Lattice Sync"
                history.append(tx)
        
        # 🚀 Level-based speed multiplier
        lvl = wallet.get("level", 1)
        speed_multiplier = {1: 1.0, 2: 2.5, 3: 5.0, 4: 10.0}.get(lvl, 1.0)
        
        return {
            "name": name, "address": address, "balance": round(wallet["balance"], 8),
            "level": lvl, "network_speed": speed_multiplier,
            "history": history, "status": "QUANTUM_ACTIVE",
            "is_proxy": is_proxy,
            "is_shadow": is_shadow
        }
