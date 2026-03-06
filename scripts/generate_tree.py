import os
import re

def extract_job(filepath):
    """파일 내용에서 직업/역할 설명을 추출합니다."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(1000) # 상단 1000자만 읽음
            
            # [설명: ...] 형식 찾기
            match_desc = re.search(r'\[설명:\s*(.*?)\]', content)
            if match_desc:
                return match_desc.group(1).strip()
            
            # **[...]** 형식 찾기 (md 파일용)
            match_bold = re.search(r'\*\*\[(.*?)\]\*\*', content)
            if match_bold:
                return match_bold.group(1).strip()
                
            # 주석 및 상단 설명 찾기
            lines = content.split('\n')
            for line in lines:
                if '🚀' in line or '🛡️' in line or '💎' in line or '🏛️' in line:
                    return line.strip()
                if ':' in line and len(line) < 100:
                    return line.strip()
            
            return "N/A (General Asset)"
    except:
        return "ERROR_READING"

def generate_empire_tree():
    root_dirs = [r"c:\lovesoong", r"c:\lovesoong\workflow_gate"]
    output_file = r"c:\lovesoong\EMPIRE_RESOURCES_TREE.txt"
    
    results = []
    seen_paths = set()

    for root_dir in root_dirs:
        if not os.path.exists(root_dir): continue
        
        for root, dirs, files in os.walk(root_dir):
            # 대량의 로그/백업 폴더 제외
            if any(x in root for x in ["LOGS_HISTORY", "backup", "__pycache__", ".git", ".agent"]):
                continue
                
            for file in files:
                filepath = os.path.join(root, file)
                
                # 중복 방지
                if filepath in seen_paths: continue
                seen_paths.add(filepath)

                # .md 파일 또는 이름에 'jam'이 포함된 파일 (대소문자 무시)
                if file.lower().endswith('.md') or 'jam' in file.lower():
                    job = extract_job(filepath)
                    results.append({
                        "Name": file,
                        "Path": filepath.replace(root_dir, "ROOT"),
                        "Job": job
                    })

    # 결과 저장
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("="*100 + "\n")
        f.write(f" 👑 PHOENIX EMPIRE - FULL RESOURCE TREE (MD & JAM SPECIALISTS)\n")
        f.write(f" [GENERATE TIME] {os.popen('echo %date% %time%').read().strip()}\n")
        f.write("="*100 + "\n\n")
        
        f.write(f"{'NAME':<35} | {'JOB/ROLE':<50} | {'LOCATION'}\n")
        f.write("-" * 150 + "\n")
        
        for r in sorted(results, key=lambda x: x['Name']):
            f.write(f"{r['Name']:<35} | {r['Job'][:50]:<50} | {r['Path']}\n")

    print(f"Empire Tree generated successfully at: {output_file}")

if __name__ == "__main__":
    generate_empire_tree()
