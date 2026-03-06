from .pqc_ledger import PQCLedger
from .pqc_mining import PQCMiningEngine
from .pqc_transfer import PQCTransferEngine
from .pqc_rwa import PQCRWAEngine
from .pqc_decree import PQCDecreeEngine
from .pqc_gateway import PQCNetworkGateway

class QuantumCoinEngine:
    """🛡️ [PHOENIX-V12] Imperial Engine Facade"""
    def __init__(self):
        # State
        self.pqc_price_krw = 1000.0
        self.target_price = 1000.0
        self.quantum_speed = 1.0
        self.gold_backed_reserve_kg = 500.0
        
        # Sub-Engines
        self.ledger = PQCLedger(self)
        self.mining = PQCMiningEngine(self)
        self.transfer_engine = PQCTransferEngine(self) # Renamed internally but mapped below
        self.rwa = PQCRWAEngine(self)
        self.decree = PQCDecreeEngine(self)
        self.gateway = PQCNetworkGateway(self)

    # --- Backward Compatibility Mappings ---
    def _log(self, msg): self.ledger.log(msg)
    
    def mine_pqc(self, agent_name, amount):
        return self.mining.mine(agent_name, amount)
    
    def transfer_pqc(self, s, r, a):
        return self.transfer_engine.transfer(s, r, a)
        
    def batch_transfer_pqc(self, transfers):
        return self.transfer_engine.batch_transfer(transfers)
        
    def get_wallet_address(self, name):
        return self.ledger.load_state()["wallets"].get(name, {}).get("address")
        
    def get_wallet_info(self, address):
        return self.ledger.get_wallet_info(address)
        
    def stabilize_price(self):
        return self.rwa.stabilize_price()
        
    def execute_treasury_buyback(self):
        self.rwa.execute_buyback()
        
    def execute_imperial_decree(self, d_id, a_type, params):
        return self.decree.execute(d_id, a_type, params)
        
    def issue_physical_rwa_pqc(self, w_name, amount):
        return self.rwa.issue_physical_rwa(w_name, amount)
        
    def get_mining_stats(self):
        return self.mining.get_stats()

    @property
    def transfer(self): return self.transfer_engine

# 🛡️ Global Singleton Instance
pqc_engine = QuantumCoinEngine()
