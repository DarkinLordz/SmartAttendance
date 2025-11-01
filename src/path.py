import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
DATA_DIR = os.path.join(ROOT_DIR, "data")
FACES_DIR = os.path.join(DATA_DIR, "faces")
SRC_DIR = os.path.join(ROOT_DIR, "src")

ATTENDANCE_CSV = os.path.join(DATA_DIR, "attendance.csv")
STUDENTS_CSV = os.path.join(DATA_DIR, "students.csv")

RECOGNIZE_WAV = os.path.join(ASSETS_DIR, "recognize.wav")