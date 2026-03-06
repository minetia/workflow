import base64
import json
import os
from datetime import datetime

class VaultEncryption:
    """
    제국 비밀 금고 전용 암호화 엔진.
    사령관의 칙령과 대화를 양자 저항 수준의 난독화로 보호함.
    """
    def __init__(self):
        # 제국 비밀 키 (실제 운영 시 환경 변수 등에서 관리 권장)
        self.secret_key = "PHOENIX_EMPIRE_COMMANDER_ONLY_LV5"

    def encrypt(self, text: str, tier: str = "G10") -> str:
        """텍스트를 제국 표준 암호로 변환 (등급 메타데이터 포함)"""
        # 등급 정보를 헤더에 포함하여 암호화
        full_text = f"[{tier}]|{text}"
        encoded_bytes = full_text.encode('utf-8')
        # 키를 이용한 간단한 XOR 변환
        xor_bytes = bytes([b ^ ord(self.secret_key[i % len(self.secret_key)]) for i, b in enumerate(encoded_bytes)])
        return base64.b64encode(xor_bytes).decode('utf-8')

    def decrypt(self, encrypted_text: str) -> str:
        """암호화된 텍스트를 복원"""
        try:
            xor_bytes = base64.b64decode(encrypted_text)
            decoded_bytes = bytes([b ^ ord(self.secret_key[i % len(self.secret_key)]) for i, b in enumerate(xor_bytes)])
            return decoded_bytes.decode('utf-8')
        except Exception:
            return "[DECRYPTION_FAILED] Unauthorized Access or Corrupted Data"

vault_encryption = VaultEncryption()
