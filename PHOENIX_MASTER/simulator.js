// ==========================================
// NEXUS HYPERCORE ENGINE (Live PNL Simulation Ver)
// ==========================================

class HyperCore {
    constructor() {
        this.socket = null;
        this.target = "KRW-BTC";
        this.isRunning = false;
        
        // 💰 Imperial Equity: Synchronized to 10M for Phase 70 Alignment
        this.balance = 10000000; 
        this.initialBalance = 10000000;
        this.syncInterval = null; 
        this.tradeHistoryCount = 0; 
        
        // 차트 및 데이터
        this.chart = null;
        this.series = null;
        this.prices = [];
        this.orderbook = { asks: [], bids: [] };
        
        this.useWidget = (typeof LightweightCharts === 'undefined');
    }

    init() {
        // Imperial Boot Sequence
        setTimeout(() => {
            const overlay = document.getElementById('loadingOverlay');
            if(overlay) {
                overlay.style.opacity = '0';
                setTimeout(() => overlay.style.display = 'none', 800);
            }
        }, 2000);

        try {
            this.log("NEXUS HYPERCORE: QUANTUM LINK ESTABLISHED", "SYS");
            this.updateWallet(); 
            
            try {
                this.initChart();
            } catch(e) {
                this.useWidget = true;
                this.initChart(); 
            }

            this.initDepthChart();
            this.connectUpbit(this.target);
            requestAnimationFrame(() => this.renderDepth());
            
        } catch (error) {
            this.log("RE-INITIALIZATION FAILURE: CORE LATTICE BREACH", "ERR");
        }
    }

    initChart() {
        const container = document.getElementById('chart-container');
        container.innerHTML = ''; 

        if (this.useWidget) {
            new TradingView.widget({
                "container_id": "chart-container",
                "symbol": `UPBIT:${this.target.replace('KRW-','')}KRW`,
                "interval": "1",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "rgba(0,0,0,0)",
                "enable_publishing": false,
                "hide_side_toolbar": true,
                "autosize": true
            });
            this.log("CHART MODE: IMPERIAL WIDGET", "SYS");
        } else {
            this.chart = LightweightCharts.createChart(container, {
                layout: { background: { color: 'transparent' }, textColor: '#94a3b8' },
                grid: { vertLines: { color: 'rgba(255,255,255,0.03)' }, horzLines: { color: 'rgba(255,255,255,0.03)' } },
                timeScale: { borderVisible: false, timeVisible: true, secondsVisible: true },
                rightPriceScale: { borderVisible: false },
                autoSize: true
            });
            
            this.series = this.chart.addCandlestickSeries({
                upColor: '#f43f5e', downColor: '#3b82f6',
                borderUpColor: '#f43f5e', borderDownColor: '#3b82f6',
                wickUpColor: '#f43f5e', wickDownColor: '#3b82f6',
            });

            this.injectDummyData();
            this.log("CHART MODE: 4D PRO ENGINE", "SYS");
        }
    }

    injectDummyData() {
        if(!this.series) return;
        const data = [];
        let price = 50000000;
        const now = Math.floor(Date.now()/1000);
        for(let i=0; i<100; i++) {
            const time = now - (100-i)*60;
            const close = price * (1 + (Math.random()-0.5)*0.002);
            data.push({ 
                time, open: price, high: Math.max(price, close)*1.0005, 
                low: Math.min(price, close)*0.9995, close 
            });
            price = close;
        }
        this.series.setData(data);
    }

    connectUpbit(code) {
        if(this.socket) this.socket.close();
        try {
            this.socket = new WebSocket("wss://api.upbit.com/websocket/v1");
            this.socket.binaryType = "arraybuffer";
            this.socket.onopen = () => {
                const payload = [
                    { ticket: "NEXUS" },
                    { type: "ticker", codes: [code] },
                    { type: "orderbook", codes: [code] },
                    { type: "trade", codes: [code] } 
                ];
                this.socket.send(JSON.stringify(payload));
                this.log(`CONNECTED: ${code}`, "SYS");
            };

            this.socket.onmessage = (e) => {
                const enc = new TextDecoder("utf-8");
                const data = JSON.parse(enc.decode(e.data));
                if(data.type === 'ticker') this.processTicker(data);
                if(data.type === 'orderbook') this.orderbook = { 
                    asks: data.orderbook_units.map(u=>({p:u.ask_price, s:u.ask_size})), 
                    bids: data.orderbook_units.map(u=>({p:u.bid_price, s:u.bid_size})) 
                };
                if(data.type === 'trade') this.processTrade(data);
            };
        } catch(e) {
            this.log("CONNECTION FAILED.", "WARN");
        }
    }

    processTicker(data) {
        const el = document.getElementById('ticker-price');
        const ch = document.getElementById('ticker-change');
        if(!el || !ch) return;
        
        el.innerText = data.trade_price.toLocaleString();
        const rate = (data.signed_change_rate * 100).toFixed(2);
        
        el.style.color = data.change === 'RISE' ? 'var(--up)' : 'var(--down)';
        ch.innerText = `${rate}%`;
        ch.style.color = el.style.color;

        if (!this.useWidget && this.series) {
            const now = Math.floor(Date.now() / 1000);
            this.series.update({
                time: now,
                open: data.opening_price,
                high: data.high_price,
                low: data.low_price,
                close: data.trade_price
            });
        }
    }

    processTrade(data) {
        if(this.isRunning) return; 
        const feed = document.getElementById('trade-feed');
        if(!feed) return;

        const div = document.createElement('div');
        div.className = `feed-row ${data.ask_bid==='BID'?'buy':'sell'}`;
        const time = new Date(data.timestamp).toLocaleTimeString('ko-KR',{hour12:false});
        div.innerHTML = `
            <span>${time}</span>
            <span>${data.ask_bid==='BID'?'매수':'매도'}</span>
            <span>${data.trade_price.toLocaleString()}</span>
            <span>${data.trade_volume.toFixed(4)}</span>
        `;
        feed.prepend(div);
        if(feed.children.length > 20) feed.removeChild(feed.lastChild);
    }

    initDepthChart() {
        const canvas = document.getElementById('depth-chart');
        if(!canvas) return;
        this.depthCtx = canvas.getContext('2d');
        const resize = () => {
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
        };
        window.addEventListener('resize', resize);
        resize();
    }

    renderDepth() {
        const ctx = this.depthCtx;
        if(!ctx) return;
        const w = ctx.canvas.width;
        const h = ctx.canvas.height;
        ctx.clearRect(0, 0, w, h);

        const asks = this.orderbook.asks;
        const bids = this.orderbook.bids;
        if(!asks.length || !bids.length) {
            requestAnimationFrame(() => this.renderDepth());
            return;
        }

        const mid = w / 2;
        const maxVol = Math.max(asks.reduce((a,b)=>a+b.s,0), bids.reduce((a,b)=>a+b.s,0));

        ctx.fillStyle = 'rgba(207, 48, 74, 0.3)';
        ctx.beginPath();
        ctx.moveTo(mid, h);
        let accBid = 0;
        bids.forEach((b, i) => {
            accBid += b.s;
            ctx.lineTo(mid - (i/bids.length)*mid, h - (accBid/maxVol)*h);
        });
        ctx.lineTo(0, h);
        ctx.fill();

        ctx.fillStyle = 'rgba(18, 97, 196, 0.3)';
        ctx.beginPath();
        ctx.moveTo(mid, h);
        let accAsk = 0;
        asks.forEach((a, i) => {
            accAsk += a.s;
            ctx.lineTo(mid + (i/asks.length)*mid, h - (accAsk/maxVol)*h);
        });
        ctx.lineTo(w, h);
        ctx.fill();

        requestAnimationFrame(() => this.renderDepth());
    }

    // =========================================================
    // 🧠 [5] 파이썬 백엔드(The Jams) 연동 및 손익(PNL) 시뮬레이션
    // =========================================================
    async fetchBackendData() {
        if (!this.isRunning) return; 
        
        try {
            const res = await axios.get('/api/trader/status');
            const data = res.data;

            // 파이썬 잼 실시간 체결 내역 렌더링
            if(data.recent_trades && data.recent_trades.length > 0) {
                this.renderAITrades(data.recent_trades);

                // 💸 [핵심] 새로운 거래가 포착될 때마다 5천만 원에서 손익(PNL) 발생
                if (this.tradeHistoryCount === 0) {
                    // 최초 연결 시 거래 횟수만 기억 (잔고는 5천 유지)
                    this.tradeHistoryCount = data.recent_trades.length;
                } else if (data.recent_trades.length > this.tradeHistoryCount) {
                    // 잼(Jam)들이 새로운 거래를 성사시켰음!
                    const newTrades = data.recent_trades.length - this.tradeHistoryCount;
                    
                    for(let i=0; i<newTrades; i++) {
                        // -0.8% ~ +1.5% 사이의 리얼한 수익률 랜덤 생성 (트레이닝 시뮬레이션용)
                        const pnlPercent = (Math.random() * 2.3) - 0.8; 
                        const pnlAmount = this.balance * (pnlPercent / 100);
                        this.balance += pnlAmount; // 잔고 업데이트

                        const pnlSign = pnlAmount > 0 ? "+" : "";
                        const pnlColor = pnlAmount > 0 ? "#f43f5e" : "#3b82f6"; 
                        
                        // 화면 로그에 정산 결과 출력
                        this.log(`<span style="color:${pnlColor}">[SETTLEMENT] ${pnlSign}${Math.round(pnlAmount).toLocaleString()} KRW (${pnlSign}${pnlPercent.toFixed(2)}%)</span>`, "PNL");
                    }
                    
                    // 횟수 갱신 및 UI 업데이트
                    this.tradeHistoryCount = data.recent_trades.length;
                    this.updateWallet();
                }
            }

            if(data.logs && data.logs.length > 0) {
                this.renderAILogs(data.logs);
            }
        } catch(e) {
            console.warn("Imperial Sync Error.");
        }
    }

    renderAITrades(trades) {
        const feed = document.getElementById('trade-feed');
        if(!feed) return;
        feed.innerHTML = ''; 
        trades.slice().reverse().forEach(trade => {
            const isBuy = trade.side === 'BUY';
            const div = document.createElement('div');
            div.className = `feed-row ${isBuy ? 'buy' : 'sell'}`;
            const timeStr = trade.time ? trade.time.split(' ')[1] : '';
            
            div.innerHTML = `
                <span><i class="fas fa-brain" style="color:var(--quantum-cyan); font-size:0.8em;"></i> ${timeStr}</span>
                <span>${isBuy ? 'NEURAL_BUY' : 'NEURAL_SELL'}</span>
                <span>${Number(trade.price).toLocaleString()}</span>
                <span>${Number(trade.amount).toFixed(4)}</span>
            `;
            feed.appendChild(div);
        });
    }

    renderAILogs(logs) {
        const box = document.getElementById('ai-log');
        if(!box) return;
        box.innerHTML = '';
        logs.slice().reverse().forEach(log => {
            const div = document.createElement('div');
            div.className = 'log-entry';
            const time = log.time || new Date().toLocaleTimeString('ko-KR',{hour12:false});
            const msg = log.activity || log;
            div.innerHTML = `<span class="log-sys" style="color:#00f3ff;">[JAM]</span> <span style="color:#888;">[${time}]</span> ${msg}`;
            box.appendChild(div);
        });
    }

    updateWallet() {
        const el = document.getElementById('core-balance');
        if(!el) return;
        
        el.innerText = Math.floor(this.balance).toLocaleString();
        
        // Dynamic Glow based on profit from initial 10M
        if(this.balance > 10000000) {
            el.style.color = "var(--up)"; 
            el.style.textShadow = "0 0 15px rgba(244, 63, 94, 0.4)";
        } else if (this.balance < 10000000) {
            el.style.color = "var(--down)"; 
            el.style.textShadow = "0 0 15px rgba(59, 130, 246, 0.4)";
        } else {
            el.style.color = "#fff"; 
            el.style.textShadow = "none";
        }
    }

    log(msg, type) {
        const box = document.getElementById('ai-log');
        if(!box) return;
        const div = document.createElement('div');
        div.className = 'log-entry';
        div.innerHTML = `<span class="log-${type.toLowerCase()}" style="color:#00f3ff;">[${type}]</span> ${msg}`;
        box.prepend(div);
        if(box.children.length > 20) box.removeChild(box.lastChild);
    }
}

// =========================================================
// 🎛️ 실행 및 이벤트 제어
// =========================================================
const core = new HyperCore();
window.onload = () => core.init();

function changeCore(val) {
    core.target = val;
    core.log(`TARGET SCAN: ${val}`, "SYS");
    core.connectUpbit(val);
    if(core.useWidget) core.initChart(); 
}

function toggleHyper() {
    core.isRunning = !core.isRunning;
    const btn = document.getElementById('btn-hyper');
    const sentText = document.getElementById('sent-text');
    
    if(core.isRunning) {
        btn.innerHTML = '<i class="fas fa-spin fa-sync"></i> NEURAL LINK ACTIVE';
        btn.classList.add('active');
        if(sentText) sentText.innerText = "QUANTUM LATTICE ENGAGED";
        
        // 파이썬 잼 데이터 수집 시작 (1.5초 간격)
        core.syncInterval = setInterval(() => core.fetchBackendData(), 1500);
        core.log("IMPERIAL AI SQUADRON: ACTIVE DATA STREAM TRANSMITTING", "SYS");
    } else {
        btn.innerHTML = '<i class="fas fa-power-off"></i> START ENGINE';
        btn.classList.remove('active');
        if(sentText) sentText.innerText = "QUANTUM SYNC STABLE";
        
        clearInterval(core.syncInterval);
        core.log("NEURAL LINK DISCONNECTED: SYSTEM STANDBY", "SYS");
    }
}