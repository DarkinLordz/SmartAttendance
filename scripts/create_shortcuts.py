import win32com.client # This only works on windows, don't try on linux
import sys # I expect linux users to know how to create shortcuts, so I won't add support for it.
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from path import SRC_DIR, STUDENTS_CSV, ATTENDANCE_CSV, FACES_DIR

def create_shortcut(target_path, shortcut_name):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    shortcut_path = os.path.join(desktop, f"{shortcut_name}.lnk")

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.Targetpath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.IconLocation = target_path
    shortcut.save()

create_shortcut(FACES_DIR, "FACES")
create_shortcut(STUDENTS_CSV, "STUDENTS")
create_shortcut(ATTENDANCE_CSV, "ATTENDANCE")
create_shortcut(os.path.join(SRC_DIR, "gui.pyw"), "GUI")
create_shortcut(os.path.join(SRC_DIR, "recognize.py"), "START")