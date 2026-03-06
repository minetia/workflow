import os

def find_file(root_dir, target_name):
    print(f"[SEARCHING] Starting deep scan in {root_dir}...")
    found_paths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if target_name.lower() in file.lower() and file.endswith(".exe"):
                full_path = os.path.join(root, file)
                print(f"[FOUND] {full_path}")
                found_paths.append(full_path)
    return found_paths

if __name__ == "__main__":
    # C 드라이브 전체 스캔 (사령관님의 주 저장 장치)
    targets = find_file("C:\\", "Antigravity")
    
    if not targets:
        print("[REPORT] Antigravity 실행 파일을 찾을 수 없습니다. 설치가 취소되었거나 다른 드라이브에 있을 수 있습니다.")
    else:
        print(f"\n[FINAL REPORT] 총 {len(targets)}개의 파일을 발견했습니다.")