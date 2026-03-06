import os
import json
from datetime import datetime

class EmpireSurveyor:
    """
    제국 영토 감시자: workflow 디렉토리를 스캔하여 제국루트.txt를 최신 상태로 유지
    """
    def __init__(self, root_dir=r'C:\Users\loves\workflow'):
        self.root_dir = root_dir
        self.route_map_path = os.path.join(self.root_dir, '제국루트.txt')
        self.scan_ignore = ['.git', '__pycache__', 'node_modules', '.gemini', 'tmp', 'data']
        
    def scan_and_update(self):
        current_structure = self._get_directory_structure(self.root_dir)
        with open(self.route_map_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 새로운 섹션 추가 준비 (이미 존재하는지 확인 후)
        new_entries = []
        for parent, dirs in current_structure.items():
            for d in dirs:
                path_str = os.path.relpath(os.path.join(parent, d), self.root_dir)
                # 이미 텍스트 파일에 해당 경로가 언급되어 있는지 확인 (단순 문자열 매칭)
                if d not in content and path_str not in content:
                    dept_name = self._infer_department_name(path_str)
                    new_entries.append(f"    ├── 📂 {d} ({dept_name})\n    │   └── Location: {path_str}")

        if new_entries:
            update_str = f"\n\n[🛰️ NEW IMPERIAL EXPANSION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n"
            update_str += "│\n" + "\n".join(new_entries)
            
            # 마지막 업데이트 시간 갱신 (상단부)
            # [LAST UPDATE] 2026-03-02 14:22:00
            import re
            new_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            content = re.sub(r'\[LAST UPDATE\] \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', f'[LAST UPDATE] {new_date}', content)
            
            with open(self.route_map_path, 'w', encoding='utf-8') as f:
                f.write(content + update_str)
            return {"success": True, "added": len(new_entries)}
        
        return {"success": True, "added": 0, "message": "No new territories detected."}

    def _get_directory_structure(self, root):
        structure = {}
        for root, dirs, files in os.walk(root):
            # 필터링
            dirs[:] = [d for d in dirs if d not in self.scan_ignore]
            structure[root] = dirs
            # 너무 깊게 들어가지 않음 (제국 루트는 주요 부서 중심)
            if root.count(os.sep) - self.root_dir.count(os.sep) >= 2:
                dirs[:] = [] 
        return structure

    def _infer_department_name(self, rel_path):
        if "NETWORK_DIVISION" in rel_path: return "Network Division Alpha-Sector"
        if "PHOENIX_MASTER" in rel_path: return "Imperial High Command"
        if "QUANTUM_CORE" in rel_path: return "Quantum Energy Sector"
        if "routes" in rel_path: return "Imperial Connection Gateway"
        return "New Imperial Territory"

empire_surveyor = EmpireSurveyor()

if __name__ == "__main__":
    # 단독 실행 시 즉시 스캔
    print(empire_surveyor.scan_and_update())
