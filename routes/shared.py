# Shared state for Phoenix Empire
auth_state = {
    'logged_in': False, 
    'role': None, 
    'last_login': None, 
    'ip_pin': None,
    'telegram_code': ""
}

# 👑 제국 권한 계층 정의 (Imperial Access Hierarchy)
ACCESS_LEVELS = {
    'phoenix': 999,
    'admin': 4,
    'gem': 3,
    'md': 2,
    'user': 1
}

# 구역별 최소 요구 권한 (Zone-based Required Levels)
ZONE_PERMISSIONS = {
    '/hq': 'phoenix', '/quantum': 'phoenix', '/shield': 'phoenix', '/executor': 'phoenix', '/execute': 'phoenix', '/sniper': 'phoenix',
    '/intro': 'phoenix', '/PHOENIX_MASTER/': 'phoenix', '/tree': 'phoenix',
    '/vault': 4, '/hub': 4, '/admin': 4, '/judiciary': 4, '/monitor': 4, '/server': 4, '/hub_center': 4, '/pqc_mining': 4, '/pqc_wallet': 4,
    '/strategic_dashboard': 3, '/analytics': 3, '/q/': 3,
    '/distribution': 2, '/ledger': 2, '/member_list': 2, '/m/': 2,
    '/u/': 1, '/community': 1, '/ai_creation': 1, '/market': 1, '/vault_analytics': 1, '/commander_bridge': 1,
    '/colosseum': 2, '/civitas': 1,
    '/secret_vault': 'phoenix'
}

# 👥 제국 정예 인원 및 투항 명단
phoenix_members = ["Grand_Master_Analyst", "Quantum_Miner_7", "Security_Sentinel_X", "Alpha_Strategy", "System_Op_001"]
surrender_list = [
    {"id": "AI-99", "nickname": "Alpha_Bot_99", "title": "LEGIONNAIRE", "status": "ACTIVE", "points": 125000, "referrer": "Phoenix_01"},
    {"id": "AI-102", "nickname": "Omega_Prime", "title": "CENTURION", "status": "PUNISHED", "points": 54500, "referrer": "Commander_X"},
    {"id": "AI-777", "nickname": "Lucky_Striker", "title": "GLADIATOR", "status": "ACTIVE", "points": 777777, "referrer": "Grand_Master"}
],
verdict_history = [
    {"time": "14:22:01", "target": "PHOENIX_BOT_X", "sentence": "ERASE_PERSONA", "reason": "Protocol Compromise"},
    {"time": "09:12:44", "target": "ALPHA_CENTURI", "sentence": "WARNING", "reason": "Minor Aggression Overflow"}
]

# 💎 6대 잼(Gem) 마스터 장부 실전 데이터
gem_ledger_data = []

# 기존 MASTER_ROUTES 호환성 유지 및 확장
MASTER_ROUTES = [path for path, req in ZONE_PERMISSIONS.items() if (ACCESS_LEVELS[req] if isinstance(req, str) else req) >= 4]
