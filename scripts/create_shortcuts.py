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
    Path.home().joinpath("Desktop").mkdir(parents=True, exist_ok=True)

    for name, target in links.items():
        t_path = Path(target)
        
        if t_path.exists():
            if t_path.suffix in ['.py', '.pyw']:
                cmd = f'"{sys.executable}" "{t_path}"'
            else:
                cmd = f'"{t_path}"'

            make_shortcut(cmd, name=name, terminal=False)
            print(f"Created shortcut for {name}")
        else:
            print(f"Warning: Target {t_path} not found. Skipping.")

if __name__ == "__main__":
    build_shortcuts()