/**
 * [PHOENIX_MASTER] Dashboard Engine
 * 1~5번 프리미엄 UI 모듈을 메인 INDEX.HTML에서 동적으로 띄워주는 통합 관제 스크립트
 */
console.log("🧩 [DASHBOARD_ENGINE] 통합 Iframe 컨트롤러 가동 준비.");

function loadModule(moduleId, targetElementId) {
    const modules = {
        'auto_trade': 'QUANTUM_CORE/1_automated_trading.html',
        'wealth_dist': 'DATA_VAULT/2_wealth_distribution.html',
        'risk_mgmt': 'SECURITY_SHIELD/3_risk_management.html',
        'social': 'PHOENIX_MASTER/4_social_community.html',
        'analytics': 'THE_EXECUTOR/5_global_analytics.html'
    };

    const url = modules[moduleId];
    if (!url) return;

    const targetDiv = document.getElementById(targetElementId);
    if (targetDiv) {
        targetDiv.innerHTML = `<iframe src="${url}" class="w-full h-full border-0 rounded-lg" style="min-height: 400px; box-shadow: 0 0 15px rgba(255,215,0,0.3);"></iframe>`;
    }
}

// 초기 로딩 시 기본 패널 로딩 
document.addEventListener('DOMContentLoaded', () => {
    // These IDs should match the ones in INDEX.HTML
    setTimeout(() => {
        loadModule('wealth_dist', 'whale-feed-container');
        loadModule('auto_trade', 'quantum-feed-container');
        loadModule('risk_mgmt', 'security-feed-container');
    }, 1000);
});
