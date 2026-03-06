import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class VaultManager:
    """
    제국 비밀 문서 분류 및 승인 관리 시스템.
    10개 계급(10급~1급) 및 특급으로 문서를 관리하며, 승인 요청을 처리함.
    """
    def __init__(self):
        # 문서 등급 정의
        self.TIERS = {
            "SPECIAL": "★ 특급 (IMPERIAL_TOP_SECRET)",
            "G1": "1급 (SECRET_LEVEL_1)",
            "G2": "2급 (SECRET_LEVEL_2)",
            "G3": "3급 (SECRET_LEVEL_3)",
            "G4": "4급 (SECRET_LEVEL_4)",
            "G5": "5급 (SECRET_LEVEL_5)",
            "G6": "6급 (SECRET_LEVEL_6)",
            "G7": "7급 (SECRET_LEVEL_7)",
            "G8": "8급 (SECRET_LEVEL_8)",
            "G9": "9급 (SECRET_LEVEL_9)",
            "G10": "10급 (UNCLASSIFIED_INTERNAL)"
        }
        
        # 승인 요청 큐: {request_id: {purpose, reason, status, requester, timestamp, tier}}
        self.approval_queue: Dict[str, dict] = {}
        
        # 기밀 문서 저장소 (메타데이터): {doc_id: {title, tier, encrypted_data_ref}}
        self.classified_docs: Dict[str, dict] = {
            "DOC_001": {
                "title": "제국 제1칙령 - 트레이딩 비현실성 선언",
                "tier": "SPECIAL",
                "created_at": "2026-02-28 20:51:24"
            }
        }

    def request_access(self, doc_id: str, requester: str, purpose: str, reason: str) -> str:
        """문서 열람 승인 요청 생성"""
        if doc_id not in self.classified_docs:
            return "ERROR: DOCUMENT_NOT_FOUND"
            
        request_id = str(uuid.uuid4())[:8].upper()
        self.approval_queue[request_id] = {
            "doc_id": doc_id,
            "title": self.classified_docs[doc_id]["title"],
            "tier": self.classified_docs[doc_id]["tier"],
            "requester": requester,
            "purpose": purpose,
            "reason": reason,
            "status": "PENDING",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return request_id

    def approve_request(self, request_id: str, admin_role: str) -> bool:
        """피닉스의 승인 처리"""
        if admin_role != "phoenix":
            return False
            
        if request_id in self.approval_queue:
            self.approval_queue[request_id]["status"] = "APPROVED"
            return True
        return False

    def get_pending_requests(self) -> List[dict]:
        """미결 승인 요청 목록 반환"""
        return [dict(req, id=rid) for rid, req in self.approval_queue.items() if req["status"] == "PENDING"]

    def check_access_status(self, request_id: str) -> Optional[dict]:
        """승인 상태 확인 및 데이터 반환 가능 여부 체크"""
        return self.approval_queue.get(request_id)

vault_manager = VaultManager()
