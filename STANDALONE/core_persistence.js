/**
 * SystemCore Standalone Persistence Layer (v1.0)
 * Manages shared state across local HTML files.
 */

const SC_CONFIG = {
    INIT_USDT: 10000,
    LOG_MAX_ENTRIES: 50,
    STORAGE_KEYS: {
        BALANCE: 'sc_usdt_balance',
        PORTFOLIO: 'sc_portfolio',
        TRADERS: 'sc_traders_state',
        LOG: 'sc_system_log',
        ROUND: 'sc_current_round',
        INIT_CAPITAL: 'sc_initial_capital'
    }
};

const Persistence = {
    // ─── INITIALIZATION ───
    init() {
        if (!localStorage.getItem(SC_CONFIG.STORAGE_KEYS.BALANCE)) {
            localStorage.setItem(SC_CONFIG.STORAGE_KEYS.BALANCE, SC_CONFIG.INIT_USDT.toString());
        }
        if (!localStorage.getItem(SC_CONFIG.STORAGE_KEYS.INIT_CAPITAL)) {
            localStorage.setItem(SC_CONFIG.STORAGE_KEYS.INIT_CAPITAL, SC_CONFIG.INIT_USDT.toString());
        }
        if (!localStorage.getItem(SC_CONFIG.STORAGE_KEYS.PORTFOLIO)) {
            localStorage.setItem(SC_CONFIG.STORAGE_KEYS.PORTFOLIO, '{}');
        }
        if (!localStorage.getItem(SC_CONFIG.STORAGE_KEYS.LOG)) {
            localStorage.setItem(SC_CONFIG.STORAGE_KEYS.LOG, '[]');
        }
        console.log("💠 SystemCore Persistence Initialized");
    },

    // ─── BALANCE & CAPITAL ───
    getBalance() {
        return parseFloat(localStorage.getItem(SC_CONFIG.STORAGE_KEYS.BALANCE) || SC_CONFIG.INIT_USDT);
    },

    setBalance(val) {
        localStorage.setItem(SC_CONFIG.STORAGE_KEYS.BALANCE, val.toString());
        this.log('BALANCE_UPDATE', `Balance updated to $${val.toFixed(2)}`);
    },

    getInitialCapital() {
        return parseFloat(localStorage.getItem(SC_CONFIG.STORAGE_KEYS.INIT_CAPITAL) || SC_CONFIG.INIT_USDT);
    },

    // ─── PORTFOLIO (COINS) ───
    getPortfolio() {
        return JSON.parse(localStorage.getItem(SC_CONFIG.STORAGE_KEYS.PORTFOLIO) || '{}');
    },

    savePortfolio(data) {
        localStorage.setItem(SC_CONFIG.STORAGE_KEYS.PORTFOLIO, JSON.stringify(data));
    },

    // ─── 100 TRADERS STATE ───
    getTradersState() {
        return JSON.parse(localStorage.getItem(SC_CONFIG.STORAGE_KEYS.TRADERS) || '[]');
    },

    saveTradersState(traders, round) {
        localStorage.setItem(SC_CONFIG.STORAGE_KEYS.TRADERS, JSON.stringify(traders));
        localStorage.setItem(SC_CONFIG.STORAGE_KEYS.ROUND, round.toString());
    },

    getRound() {
        return parseInt(localStorage.getItem(SC_CONFIG.STORAGE_KEYS.ROUND) || '1');
    },

    // ─── LOGGING (COMPACT) ───
    log(type, message) {
        const log = JSON.parse(localStorage.getItem(SC_CONFIG.STORAGE_KEYS.LOG) || '[]');
        const entry = {
            t: new Date().toLocaleTimeString(),
            k: type, // k for kind/type
            m: message // m for msg
        };
        log.unshift(entry);
        if (log.length > SC_CONFIG.LOG_MAX_ENTRIES) log.pop();
        localStorage.setItem(SC_CONFIG.STORAGE_KEYS.LOG, JSON.stringify(log));

        // Dispatch custom event for real-time UI updates
        window.dispatchEvent(new CustomEvent('sc_log_update', { detail: entry }));
    },

    getLogs() {
        return JSON.parse(localStorage.getItem(SC_CONFIG.STORAGE_KEYS.LOG) || '[]');
    },

    clearData() {
        if (confirm("모든 데이터를 초기화하시겠습니까?")) {
            localStorage.clear();
            location.reload();
        }
    }
};

// Auto-init
Persistence.init();
