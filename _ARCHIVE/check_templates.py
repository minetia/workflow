import os
import re

loader_paths = ['.', 'templates', 'PHOENIX_MASTER', 'PHOENIX_CIVITAS', 'DATA_VAULT', 'QUANTUM_CORE', 'workflow_gate']
templates_dir = 'templates'

with open('routes/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

templates = re.findall(r"render_template\(['\"]([^'\"]+)['\"]", content)
unique_templates = set(templates)

print(f"Checking {len(unique_templates)} unique templates...")

missing = []
for t in unique_templates:
    found = False
    for path in loader_paths:
        full_path = os.path.join(path, t)
        if os.path.exists(full_path):
            found = True
            # print(f"Found: {t} in {path}")
            break
    if not found:
        missing.append(t)

if missing:
    print("\n--- MISSING TEMPLATES ---")
    for m in missing:
        print(m)
else:
    print("\nAll templates found!")
