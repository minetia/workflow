/**
 * PHOENIX EMPIRE | VAULT & TRADER ENGINE DISPLAY
 * Handles real-time polling and UI updates for the Strategic Dashboard.
 */

class VaultDisplay {
    constructor() {
        this.ctx = document.getElementById('vaultChart').getContext('2d');
        this.chart = null;
        this.historyData = {
            labels: [],
            total: [],
            tax: []
        };
        this.initChart();
        this.startPolling();
    }

    initChart() {
        this.chart = new Chart(this.ctx, {
            type: 'line',
            data: {
                labels: this.historyData.labels,
                datasets: [
                    {
                        label: 'Gross Asset',
                        data: this.historyData.total,
                        borderColor: '#ffd700',
                        backgroundColor: 'rgba(255, 215, 0, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 0
                    },
                    {
                        label: 'Total Tax Collected',
                        data: this.historyData.tax,
                        borderColor: '#d97706',
                        borderWidth: 1,
                        borderDash: [5, 5],
                        fill: false,
                        tension: 0,
                        pointRadius: 0
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { display: false },
                    y: {
                        grid: { color: 'rgba(255,255,255,0.05)' },
                        ticks: { color: '#64748b', font: { size: 10 } }
                    }
                }
            }
        });
    }

    async startPolling() {
        setInterval(async () => {
            try {
                const [traderRes, intelRes] = await Promise.all([
                    fetch('/api/trader/status'),
                    fetch('/api/admin/intelligence')
                ]);

                const traderData = await traderRes.json();
                const intelData = await intelRes.json();

                this.updateUI(traderData);
                this.updateIntelligence(intelData);
            } catch (error) {
                console.error("Failed to fetch Phoenix stats:", error);
            }
        }, 3000);
    }

    updateIntelligence(data) {
        const intelFeed = document.getElementById('intelligence-feed');
        if (!intelFeed) return;

        intelFeed.innerHTML = [...data.logs].reverse().map(log => {
            let color = 'text-blue-400';
            if (log.type === 'SYSTEM_SEC') color = 'text-green-400';
            if (log.type === 'VISITOR') color = 'text-yellow-400';

            return `
                <div class="flex space-x-2 border-b border-white/5 pb-1">
                    <span class="text-gray-600">[${log.time}]</span>
                    <span class="${color} font-black">[${log.type}]</span>
                    <span class="text-gray-400 font-bold">${log.location}</span>
                    <span class="text-gray-300">| ${log.message}</span>
                </div>
            `;
        }).join('');
        intelFeed.scrollTop = intelFeed.scrollHeight;
    }

    updateUI(data) {
        const { vault, logs, persona, orderbook, recent_trades, mode } = data;

        // Update Stats
        document.getElementById('stat-total-asset').innerText = vault.total_asset.toLocaleString(undefined, { minimumFractionDigits: 2 }) + ' KRW';
        document.getElementById('stat-total-tax').innerText = vault.tax_total.toLocaleString();
        document.getElementById('stat-virtual-vault').innerText = vault.virtual.toLocaleString();
        document.getElementById('stat-real-vault').innerText = vault.real.toLocaleString();

        const profitPct = document.getElementById('stat-profit-pct');
        profitPct.innerText = (vault.profit_percent >= 0 ? '+' : '') + vault.profit_percent + '%';
        profitPct.className = `text-xs mt-1 font-bold ${vault.profit_percent >= 0 ? 'text-green-500' : 'text-red-500'}`;

        // Update Gauges
        const totalVault = vault.virtual + vault.real || 1;
        const vPct = Math.round((vault.virtual / totalVault) * 100);
        const rPct = Math.round((vault.real / totalVault) * 100);

        document.getElementById('v-pct').innerText = vPct + '%';
        document.getElementById('r-pct').innerText = rPct + '%';
        document.getElementById('v-fill').style.width = vPct + '%';
        document.getElementById('r-fill').style.width = rPct + '%';

        // Update Persona Tag
        document.getElementById('persona-tag').innerText = persona;

        // Update Active Mode UI (주군의 명령 하사 상태 동기화)
        this.updateActiveMode(mode);

        // Update Logs
        const logContainer = document.getElementById('trader-logs');
        logContainer.innerHTML = logs.map(log => `
            <div class="log-entry">
                <span class="text-yellow-500/50 font-mono mr-2">[${log.time}]</span>
                <span class="${log.is_trade ? 'text-green-400 font-bold' : log.is_order ? 'text-blue-300' : 'text-white'}">${log.activity}</span>
                ${log.details ? `<div class="text-[9px] text-gray-500 mt-1">${log.details.msg} (Tax: ${log.details.tax_collected})</div>` : ''}
            </div>
        `).join('');
        logContainer.scrollTop = logContainer.scrollHeight;

        // Update Order Book
        this.renderOrderBook(orderbook);

        // Update Trade History
        this.renderTrades(recent_trades);

        // Update Chart
        const now = new Date().toLocaleTimeString();
        this.historyData.labels.push(now);
        this.historyData.total.push(vault.total_asset);
        this.historyData.tax.push(vault.tax_total);

        if (this.historyData.labels.length > 20) {
            this.historyData.labels.shift();
            this.historyData.total.shift();
            this.historyData.tax.shift();
        }
        this.chart.update();
    }

    renderOrderBook(ob) {
        const sellContainer = document.getElementById('ob-sells');
        const buyContainer = document.getElementById('ob-buys');
        const priceDisplay = document.getElementById('ob-price');

        if (!sellContainer || !buyContainer) return;

        const maxAmount = Math.max(
            ...ob.sells.map(o => o.amount),
            ...ob.buys.map(o => o.amount),
            0.1
        );

        sellContainer.innerHTML = ob.sells.map(o => {
            const width = (o.amount / maxAmount) * 100;
            return `
                <div class="order-row relative order-sell">
                    <div class="bar-sell" style="width: ${width}%"></div>
                    <span class="font-bold">${o.price.toLocaleString()}</span>
                    <span class="text-right">${o.amount.toFixed(4)}</span>
                </div>
            `;
        }).join('');

        buyContainer.innerHTML = ob.buys.map(o => {
            const width = (o.amount / maxAmount) * 100;
            return `
                <div class="order-row relative order-buy">
                    <div class="bar-buy" style="width: ${width}%"></div>
                    <span class="font-bold">${o.price.toLocaleString()}</span>
                    <span class="text-right">${o.amount.toFixed(4)}</span>
                </div>
            `;
        }).join('');

        if (ob.buys.length > 0 || ob.sells.length > 0) {
            const lastPrice = ob.sells[0]?.price || ob.buys[0]?.price;
            priceDisplay.innerText = lastPrice.toLocaleString();
        }
    }

    renderTrades(trades) {
        const container = document.getElementById('trade-history');
        if (!container) return;

        container.innerHTML = trades.reverse().map(t => `
            <tr class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="py-1 text-gray-500">${t.time}</td>
                <td class="text-green-400 font-bold">BUY</td>
                <td class="gold-text font-bold">${t.price.toLocaleString()}</td>
                <td class="text-white">${t.amount.toFixed(4)}</td>
                <td class="text-gray-400">${t.buyer}</td>
                <td class="text-gray-400">${t.seller}</td>
            </tr>
        `).join('');
    }

    async setMode(mode) {
        // 주군의 명령을 서버에 하달함
        try {
            const response = await fetch('/api/admin/control', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mode })
            });
            const result = await response.json();
            if (result.status === "SUCCESS") {
                console.log(`[MASTER COMMAND] AI Mode changed to: ${mode}`);
                this.updateActiveMode(mode);
            }
        } catch (error) {
            console.error("Master command failed:", error);
        }
    }

    updateActiveMode(currentMode) {
        // UI 버튼들의 활성 상태를 업데이트함
        const modes = ['STABLE', 'BALANCED', 'AGGRESSIVE', 'OVERDRIVE'];
        modes.forEach(m => {
            const btn = document.getElementById(`btn-${m}`);
            if (btn) {
                if (m === currentMode) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.phoenixDisplay = new VaultDisplay();
});
