/**
 * [PHOENIX_MASTER] 마술사의 황금 코팅 로직
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log("✨ [COATING_MAGIC]: 마술사의 황금 코팅 로직 주입 완료.");

    // 페이지 최상단 황금 띠 추가
    document.body.style.borderTop = "5px solid #ffd700";

    // 페이지 로드 시 페이드 인 효과
    document.body.style.opacity = 0;
    let opacity = 0;
    const fadeIn = setInterval(() => {
        if (opacity >= 1) clearInterval(fadeIn);
        document.body.style.opacity = opacity;
        opacity += 0.05;
    }, 50);

    // 주기적인 UI 업데이트 시뮬레이터 (INDEX.HTML 용)
    const updateDashboardFeeds = () => {
        const whaleFeed = document.getElementById('whale-feed');
        const quantumFeed = document.getElementById('quantum-feed');

        if (whaleFeed && Math.random() > 0.5) {
            const el = document.createElement('div');
            el.className = 'terminal-text text-gray-300';
            el.textContent = `[탐지] 고래 #${Math.floor(Math.random() * 9000) + 1000} | ${Math.random() > 0.5 ? 'BUY' : 'SELL'} ${Math.floor(Math.random() * 10) * 10} BTC`;
            whaleFeed.prepend(el);
            if (whaleFeed.children.length > 5) whaleFeed.lastChild.remove();
        }

        if (quantumFeed && Math.random() > 0.5) {
            const el = document.createElement('div');
            el.className = 'terminal-text text-blue-300';
            const profit = (Math.random() * 2).toFixed(2);
            el.innerHTML = `[연산] 기회 포착 ➔ 기대수익 <span class="text-green-400">+${profit}%</span>`;
            quantumFeed.prepend(el);
            if (quantumFeed.children.length > 5) quantumFeed.lastChild.remove();
        }
    };

    setInterval(updateDashboardFeeds, 2500);
});