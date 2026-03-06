/**
 * [PHOENIX_MASTER] 커뮤니티 채팅 시뮬레이션 엔진
 */
const PhoenixChat = {
    init: function() { 
        console.log("💬 [CHAT_ENGINE]: 소통 엔진 가동 완료. 대광장 채널 오픈.");
        // 주기적으로 가상의 메시지 수신 시뮬레이션
        setInterval(this.simulateIncomingMessage, 8000);
    },
    
    send: function(sender, msg) { 
        console.log(`[${sender}]: ${msg}`); 
    },
    
    simulateIncomingMessage: function() {
        const users = ["agent_alpha", "quantum_bot", "master_loves", "system_notifier"];
        const messages = [
            "현재 시장 변동성 3.2% 관측.",
            "수익 실현 완료.",
            "새로운 고래 지갑 탐지됨.",
            "사령부 지시 대기 중."
        ];
        
        const user = users[Math.floor(Math.random() * users.length)];
        const msg = messages[Math.floor(Math.random() * messages.length)];
        
        console.log(`[CHAT] ${user}: ${msg}`);
    }
};

document.addEventListener('DOMContentLoaded', () => {
    PhoenixChat.init();
});