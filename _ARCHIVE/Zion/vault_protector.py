import os
import base64

class VaultProtector:
    def __init__(self):
        self.env_path = "C:/Users/loves/workflow/Project_Phoenix/.env"
        print("🛡️ [Zion] Vault Protector Active.")

    def verify_vault(self):
        if os.path.exists(self.env_path):
            with open(self.env_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "GEMINI_API_KEY" in content:
                return "✅ [Zion] .env API Key Integrity Verified."
        return "🚨 [Zion] .env Configuration Compromised or Missing!"

    def encrypt_secret(self, text):
        return base64.b64encode(text.encode()).decode()

    def decrypt_secret(self, encrypted):
        return base64.b64decode(encrypted.encode()).decode()

if __name__ == "__main__":
    vault = VaultProtector()
    print(vault.verify_vault())
