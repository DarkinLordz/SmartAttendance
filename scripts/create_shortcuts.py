import sys
from pathlib import Path
from pyshortcuts import make_shortcut

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"

sys.path.append(str(SRC_DIR))
try:
    from path import STUDENTS_CSV, ATTENDANCE_CSV, FACES_DIR
except ImportError:
    print("Error: Could not find path.py in src directory.")
    sys.exit(1)

links = {
    "Faces": FACES_DIR,
    "Students": STUDENTS_CSV,
    "Attendance": ATTENDANCE_CSV,
    "Gui": SRC_DIR / "gui.pyw",
    "Start": SRC_DIR / "recognize.py"
}

def build_shortcuts():
    for name, target in links.items():
        target_path = Path(target)
        
        if target_path.exists():
            make_shortcut(str(target_path), name=name, terminal=False)
            print(f"Created shortcut for {name}")
        else:
            print(f"Warning: Target {target_path} not found. Skipping.")

if __name__ == "__main__":
    build_shortcuts()