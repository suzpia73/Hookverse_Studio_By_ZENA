import shutil
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CEO_DIR = os.path.join(HERE, "_company", "_agents", "ceo")
src = os.path.join(CEO_DIR, "memory.md")
dst = os.path.join(CEO_DIR, "memory_backup_20260714.md")

if os.path.exists(src):
    shutil.copy(src, dst)
    print(f"✅ 백업 완료: {dst}")
    
    # memory.md 초기화 (최근 10라인만 남김)
    with open(src, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    header = lines[:5]
    recent = lines[-10:] if len(lines) > 15 else lines[5:]
    
    with open(src, "w", encoding="utf-8") as f:
        f.writelines(header + ["\n# --- 이전 기록 백업 완료 (memory_backup_20260714.md) ---\n\n"] + recent)
    print(f"✅ memory.md 다이어트 완료 (최근 10개 기록만 남김)")
else:
    print("❌ memory.md 파일을 찾을 수 없습니다.")
