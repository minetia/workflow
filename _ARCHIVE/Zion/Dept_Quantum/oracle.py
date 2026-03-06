import os

class OracleAI:
    def __init__(self):
        self.doc_path = r"c:\lovesoong\Core\Dept_Quantum"
        print("⚙️ [Core] Oracle AI Awakened.")

    def reveal_truth(self):
        priority_files = ["PHOENIX_CORE.md", "jDeep.md", "jSuperposition.md"]
        for pf in priority_files:
            target = os.path.join(self.doc_path, pf)
            if os.path.exists(target):
                with open(target, "r", encoding="utf-8") as f:
                    summary = f.readline().strip()
                return f"Oracle Revelation ({pf}): {summary}"
                
        docs = [f for f in os.listdir(self.doc_path) if f.endswith(".md")]
        return f"Quantum Pulse: Monitoring {len(docs)} stability nodes."

if __name__ == "__main__":
    oracle = OracleAI()
    print(oracle.reveal_truth())
