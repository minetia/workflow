
# Global simulator instance using the static gem ledger data from main.py
# The ledger data will be imported lazily to avoid circular imports.

def get_simulator():
    from ..main import gem_ledger_data
    return GemTraderSimulator(gem_ledger_data)
