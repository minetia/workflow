import hashlib
import time
import random
from datetime import datetime

class PQCTransferEngine:
    def __init__(self, engine):
        self.engine = engine

    def simulate_lattice_signature(self, msg):
        sig = hashlib.sha3_256(f"lattice_{msg}_{time.time()}".encode()).hexdigest()
        self.engine.ledger.log(f"⚛️ [LATTICE] Sig: {sig[:16]}...")
        return True

    def prepare_transfer(self, s_addr, r_addr, amount):
        """Prepare phase for Quantum Lattice Transfer"""
        self.simulate_entanglement(s_addr, r_addr)
        prep_id = f"PREP-{hashlib.md5(f'{s_addr}{r_addr}{amount}{time.time()}'.encode()).hexdigest()[:8].upper()}"
        return {"success": True, "prep_id": prep_id, "steps": ["Entanglement Linked", "Lattice Channel Open"]}

    def transfer(self, s_addr, r_addr, amount, prep_id=None):
        self.simulate_lattice_signature(f"transfer_{amount}_{s_addr}")
        data = self.engine.ledger.load_state()
        s_id, r_id = data["address_book"].get(s_addr), data["address_book"].get(r_addr)
        if not s_id or not r_id or data["wallets"][s_id]["balance"] < amount:
            return {"success": False, "msg": "Insufficient or Invalid Ledger"}
        
        data["wallets"][s_id]["balance"] -= amount
        data["wallets"][r_id]["balance"] += amount
        
        txid = f"PQC-TX-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:24].upper()}"
        cert = self.generate_certificate(txid, s_addr, r_addr, amount)
        
        tx = {
            "txid": txid,
            "from": s_addr, 
            "to": r_addr, 
            "amount": amount, 
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
            "status": "CONFIRMED",
            "cert_hash": hashlib.md5(cert.encode()).hexdigest()
        }
        
        data.setdefault("transactions", []).append(tx)
        self.engine.ledger.save_state(data)
        
        # Save certificate to file for persistency
        cert_path = os.path.join(self.engine.ledger.state_dir, f"certs/{txid}.json")
        os.makedirs(os.path.dirname(cert_path), exist_ok=True)
        with open(cert_path, "w") as f: f.write(cert)
        
        return {"success": True, "tx": tx, "certificate": txid}

    def generate_certificate(self, txid, s, r, a):
        import json
        cert_data = {
            "version": "QLT-V12",
            "imperial_seal": "ANTIGRAVITY-AUTH-SIG",
            "txid": txid,
            "sender": s,
            "receiver": r,
            "amount": a,
            "asset": "PHOENIX_COIN (PQC)",
            "quantum_verification": {
                "lattice_sig": hashlib.sha256(f"{txid}lattice".encode()).hexdigest()[:16],
                "entanglement_node": "HQ-CORE-01",
                "sharding_id": s.split("-")[1] if "-" in s else "S00"
            }
        }
        return json.dumps(cert_data, indent=4)

    def batch_transfer(self, transfers):
        count = len(transfers)
        self.simulate_lattice_signature(f"batch_{count}")
        data = self.engine.ledger.load_state()
        s_count, txs = 0, []
        for t in transfers:
            sid, rid = data["address_book"].get(t['from']), data["address_book"].get(t['to'])
            if sid and rid and data["wallets"][sid]["balance"] >= t['amount']:
                data["wallets"][sid]["balance"] -= t['amount']
                data["wallets"][rid]["balance"] += t['amount']
                txs.append({"txid": f"TXID-B{hashlib.sha1(str(random.random()).encode()).hexdigest()[:12].upper()}",
                            "from": t['from'], "to": t['to'], "amount": t['amount'], "status": "BATCH"})
                s_count += 1
        data.setdefault("transactions", []).extend(txs)
        self.engine.ledger.save_state(data)
        return {"success": True, "finalized": s_count}
