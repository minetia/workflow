// File: C:\lovesoong\Castle_5_Management\js\chart_engine.js
// Role: Imperial Real-time Charting Engine (v10,000)
// Authorized by ServerMaster_MD [cite: 2026-02-28]

/**
 * [Sovereign Chart Config]
 * 사령관님의 ZRX 평단가(455 KRW)를 기준으로 차트를 초기화합니다.
 */
const commanderAvgPrice = 455; //
const ctx = document.getElementById('zrxChart').getContext('2d');
let zrxChart;

function initImperialChart() {
    zrxChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Time Labels
            datasets: [{
                label: 'ZRX/KRW Live',
                data: [],
                borderColor: '#eab308', // Imperial Gold
                borderWidth: 2,
                tension: 0.4,
                pointRadius: 0,
                fill: true,
                backgroundColor: 'rgba(234, 179, 8, 0.1)'
            }, {
                label: 'Avg Price (Sovereign Line)',
                data: [], // Fixed at 455
                borderColor: '#ef4444', // Red Line
                borderDash: [5, 5],
                borderWidth: 1,
                pointRadius: 0,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false, // Performance focus
            scales: {
                y: { grid: { color: '#1e293b' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { display: false } }
            },
            plugins: {
                legend: { display: true, labels: { color: '#f1f5f9' } }
            }
        }
    });
}

/**
 * [Live Pulse Injection]
 * jCollector를 통해 들어온 시세를 차트에 업데이트합니다.
 */
function pushChartData(currentPrice) {
    const now = new Date().toLocaleTimeString();
    
    // 데이터 추가
    zrxChart.data.labels.push(now);
    zrxChart.data.datasets[0].data.push(currentPrice);
    zrxChart.data.datasets[1].data.push(commanderAvgPrice);

    // 20개 이상의 데이터가 쌓이면 앞부분 제거 (메모리 관리)
    if (zrxChart.data.labels.length > 20) {
        zrxChart.data.labels.shift();
        zrxChart.data.datasets[0].data.shift();
        zrxChart.data.datasets[1].data.shift();
    }

    zrxChart.update();
}

document.addEventListener('DOMContentLoaded', () => {
    initImperialChart();
    console.log("[v10,000] Chart Engine Online: Tracking Avg Price 455 KRW.");
});