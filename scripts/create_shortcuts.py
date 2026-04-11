import sys
import os
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
    desktop = Path.home() / "Desktop"
    desktop.mkdir(parents=True, exist_ok=True)

    for name, target in links.items():
        t_path = Path(target).resolve()
        
        if not t_path.exists():
            print(f"Warning: Target {t_path} not found. Skipping.")
            continue

        if t_path.suffix in ['.py', '.pyw']:
            make_shortcut(str(t_path), name=name, terminal=False, executable=sys.executable)
            print(f"Created script shortcut for {name}")
        else:
            if os.name == 'nt':
                cmd = f'/c start "" "{t_path}"'
                make_shortcut("cmd.exe", name=name, args=cmd, terminal=False)
            else:
                make_shortcut(str(t_path), name=name)
            
            print(f"Created file/folder shortcut for {name}")

if __name__ == "__main__":
    build_shortcuts()