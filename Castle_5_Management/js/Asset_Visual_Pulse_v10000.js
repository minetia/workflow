// File: Asset_Visual_Pulse_v10000.js
// Role: Real-time ROI Calculator for WebMagician

const commanderAssets = {
    "ZRX": { avg: 455, amount: 29107 }, //
    "ONDO": { avg: 550, amount: 0 }    //
};

function updateAssetPulse(currentPrice) {
    const zrxROI = ((currentPrice - commanderAssets.ZRX.avg) / commanderAssets.ZRX.avg) * 100;
    document.getElementById('zrx-roi').innerText = `ROI: ${zrxROI.toFixed(2)}%`;
    
    // 주군의 아바타 경고 시스템
    if (zrxROI < -2) {
        document.body.classList.add('bg-red-900'); // 위험 감지
    }
}