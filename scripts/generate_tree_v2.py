import os
import re

def extract_job(filepath):
    """파일 내용에서 직업/역할 설명을 추출합니다."""
    try:
        # 이진 파일이나 큰 파일은 건너뛰기
        if filepath.lower().endswith(('.zip', '.exe', '.dll', '.pyc')):
            return "Binary Asset"
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(500) # 상단 500자만 읽음
            
            # [설명: ...] 형식 찾기
            match_desc = re.search(r'\[설명:\s*(.*?)\]', content)
            if match_desc:
                return match_desc.group(1).strip()
            
            # **[...]** 형식 찾기 (md 파일용)
            match_bold = re.search(r'\*\*\[(.*?)\]\*\*', content)
            if match_bold:
                return match_bold.group(1).strip()
            
            # 클래스 정의나 주석에서 힌트 찾기
            match_class = re.search(r'class\s+(\w+):', content)
            if match_class:
                return f"Class: {match_class.group(1)}"
                
            return ""
    except:
        return ""

def build_tree(path, prefix=""):
    """디렉토리를 순회하며 트리 구조를 생성합니다."""
    tree_lines = []
    
    # 제외 폴더 리스트
    exclude_dirs = ["LOGS_HISTORY", "backup", "__pycache__", ".git", ".agent", ".vscode", "node_modules", "BACKUP_CHAMBER", "BACKUP_CORE"]
    
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        return []

    # 필터링: 디렉토리이거나 .md 또는 'jam' 포함 파일만
    filtered_items = []
    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            if item not in exclude_dirs:
                # 하위에 유효한 파일이 있는지 확인 (선택 사항이지만 트리가 너무 커지면 사용)
                filtered_items.append(item)
        else:
            if item.lower().endswith('.md') or 'jam' in item.lower():
                filtered_items.append(item)

    for i, item in enumerate(filtered_items):
        item_path = os.path.join(path, item)
        connector = "└── " if i == len(filtered_items) - 1 else "├── "
        
        if os.path.isdir(item_path):
            tree_lines.append(f"{prefix}{connector}[DIR] {item}")
            extension = "    " if i == len(filtered_items) - 1 else "│   "
            tree_lines.extend(build_tree(item_path, prefix + extension))
        else:
            job = extract_job(item_path)
            job_str = f" ({job})" if job else ""
            tree_lines.append(f"{prefix}{connector}{item}{job_str}")
            
    return tree_lines

def generate_empire_tree_v2():
    root_dirs = [
        ("CORE_SYSTEM", r"c:\lovesoong"),
        ("WORKFLOW_GATE", r"c:\lovesoong\workflow_gate")
    ]
    output_file = r"c:\lovesoong\EMPIRE_STRUCTURE_TREE.txt"
    
    output_lines = []
    output_lines.append("="*100)
    output_lines.append(" 👑 PHOENIX EMPIRE - HIERARCHICAL RESOURCE TREE (MD & JAM)")
    output_lines.append(f" [GENERATE TIME] {os.popen('echo %date% %time%').read().strip()}")
    output_lines.append("="*100 + "\n")

    for label, path in root_dirs:
        if not os.path.exists(path): continue
        output_lines.append(f"[{label}] -> {path}")
        output_lines.extend(build_tree(path))
        output_lines.append("\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"Empire Hierarchical Tree generated successfully at: {output_file}")

if __name__ == "__main__":
    generate_empire_tree_v2()
