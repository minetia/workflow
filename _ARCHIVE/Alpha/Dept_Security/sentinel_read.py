import os

class SentinelArchiveAI:
    def __init__(self):
        self.doc_path = r"c:\lovesoong\Zion\Vault_Archive"
        if not os.path.exists(self.doc_path):
            os.makedirs(self.doc_path)
        print("🛡️ [Zion] Sentinel Archive Manager Active.")

    def verify_archives(self):
        docs = [f for f in os.listdir(self.doc_path) if f.endswith(".md")]
        civitas_count = len([d for d in docs if "overview" in d])
        return f"Vault Archive: {len(docs)} documents secured. {civitas_count} Civitas stability nodes active."

if __name__ == "__main__":
    sentinel = SentinelArchiveAI()
    print(sentinel.verify_archives())
