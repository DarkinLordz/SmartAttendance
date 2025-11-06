import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
DATA_DIR = os.path.join(ROOT_DIR, "data")
FACES_DIR = os.path.join(DATA_DIR, "faces")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
SRC_DIR = os.path.join(ROOT_DIR, "src")

ATTENDANCE_CSV = os.path.join(DATA_DIR, "attendance.csv")
STUDENTS_CSV = os.path.join(DATA_DIR, "students.csv")

RECOGNIZE_WAV = os.path.join(SOUNDS_DIR, "recognize.wav")

EVENTS_LOG = os.path.join(LOGS_DIR, "events.log")