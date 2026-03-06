/**
 * [PHOENIX_MASTER] Gem Chart Engine
 * Renders 2x3 grid of TradingView charts for the 6 core AIs
 */
console.log("💎 [GEM_CHART_ENGINE] Initialization sequence started.");

const gems = [
    { id: 'master', name: 'MASTER (BTC/USDT)', symbol: 'BINANCE:BTCUSDT', color: '#ffd700' },
    { id: 'aura', name: 'AURA (ETH/USDT)', symbol: 'BINANCE:ETHUSDT', color: '#a855f7' },
    { id: 'ruby', name: 'RUBY (SOL/USDT)', symbol: 'BINANCE:SOLUSDT', color: '#f87171' },
    { id: 'gold', name: 'GOLD (BNB/USDT)', symbol: 'BINANCE:BNBUSDT', color: '#fbbf24' },
    { id: 'jade', name: 'JADE (ADA/USDT)', symbol: 'BINANCE:ADAUSDT', color: '#34d399' },
    { id: 'onyx', name: 'ONYX (XRP/USDT)', symbol: 'BINANCE:XRPUSDT', color: '#4b5563' }
];

function initGemCharts() {
    const grid = document.getElementById('gem-charts-grid');
    if (!grid) return;

    // TradingView script check
    if (typeof TradingView === 'undefined') {
        console.warn("⚠️ [GEM_CHART_ENGINE] TradingView library not found. Retrying in 1s...");
        setTimeout(initGemCharts, 1000);
        return;
    }

    console.log("🚀 [GEM_CHART_ENGINE] Rendering charts...");
    grid.innerHTML = '';
    gems.forEach(gem => {
        const card = document.createElement('div');
        card.className = 'maestro-panel relative overflow-hidden h-[350px] flex flex-col p-1 mb-4';
        card.style.borderColor = gem.color + '66';
        card.innerHTML = `
            <div class="flex justify-between items-center mb-1 px-2 py-1 bg-black/40">
                <span class="text-[10px] font-black tracking-widest" style="color: ${gem.color}">${gem.name}</span>
                <div class="flex items-center space-x-1">
                    <span class="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
                    <span class="text-[8px] text-gray-500 uppercase font-bold">Live</span>
                </div>
            </div>
            <div id="chart-${gem.id}" class="flex-1 w-full rounded-b overflow-hidden" style="min-height: 280px;"></div>
        `;
        grid.appendChild(card);

        try {
            new TradingView.widget({
                "autosize": true,
                "symbol": gem.symbol,
                "interval": "1",
                "timezone": "Etc/UTC",
                "theme": "dark",
                "style": "1",
                "locale": "ko",
                "toolbar_bg": "#0b1016",
                "enable_publishing": false,
                "hide_top_toolbar": true,
                "hide_legend": true,
                "save_image": false,
                "container_id": `chart-${gem.id}`,
                "backgroundColor": "#0b1016",
                "gridColor": "rgba(255, 215, 0, 0.05)",
                "loading_screen": { "backgroundColor": "#0b1016" }
            });
        } catch (e) {
            console.error(`❌ [GEM_CHART_ENGINE] Failed to init ${gem.id}:`, e);
            document.getElementById(`chart-${gem.id}`).innerHTML = `<div class="p-10 text-[10px] text-red-900">FAILED TO LOAD ${gem.id}</div>`;
        }
    });
}

function initMainChart() {
    const container = document.getElementById('main-op-chart');
    if (!container) return;

    const chart = LightweightCharts.createChart(container, {
        layout: {
            background: { color: '#0b1016' },
            textColor: '#64748b',
        },
        grid: {
            vertLines: { color: 'rgba(255, 215, 0, 0.05)' },
            horzLines: { color: 'rgba(255, 215, 0, 0.05)' },
        },
        crosshair: {
            mode: LightweightCharts.CrosshairMode.Normal,
        },
        rightPriceScale: {
            borderColor: 'rgba(255, 215, 0, 0.2)',
        },
        timeScale: {
            borderColor: 'rgba(255, 215, 0, 0.2)',
        },
    });

    const candleSeries = chart.addCandlestickSeries({
        upColor: '#ffd700',
        downColor: '#ef4444',
        borderUpColor: '#ffd700',
        borderDownColor: '#ef4444',
        wickUpColor: '#ffd700',
        wickDownColor: '#ef4444',
    });

    // 더미 데이터 생성 (또는 API 연동 가능)
    const data = [];
    let time = Math.floor(Date.now() / 1000) - 100 * 60;
    let lastPrice = 50000;
    for (let i = 0; i < 100; i++) {
        const open = lastPrice;
        const close = open + (Math.random() - 0.5) * 100;
        const high = Math.max(open, close) + Math.random() * 20;
        const low = Math.min(open, close) - Math.random() * 20;
        data.push({ time: time + i * 60, open, high, low, close });
        lastPrice = close;
    }
    candleSeries.setData(data);

    window.addEventListener('resize', () => {
        chart.applyOptions({ width: container.clientWidth, height: container.clientHeight });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // Initial attempt with short delay
    setTimeout(() => {
        initGemCharts();
        initMainChart();
    }, 500);
});


