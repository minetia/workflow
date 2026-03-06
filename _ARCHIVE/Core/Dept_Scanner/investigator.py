import os

class InvestigatorAI:
    def __init__(self):
        self.doc_path = r"c:\lovesoong\Alpha\Dept_Scanner"
        print("🔍 [Alpha] Investigator AI Initialized.")

    def gain_insight(self):
        target_file = os.path.join(self.doc_path, "PHOENIX_EVOLUTION_LOG.md")
        if os.path.exists(target_file):
            with open(target_file, "r", encoding="utf-8") as f:
                content = f.read()[:150]
            return f"Evolutionary Intel (PHOENIX): {content}..."
        
        md_files = [f for f in os.listdir(self.doc_path) if f.endswith(".md")]
        return f"Investigating {len(md_files)} dormant scanning scrolls."

if __name__ == "__main__":
    investigator = InvestigatorAI()
    print(investigator.gain_insight())
