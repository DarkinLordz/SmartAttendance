import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(ROOT_DIR, "data")
MODEL_DIR = os.path.join(ROOT_DIR, "model")
FACE_DIR = os.path.join(DATA_DIR, "face")
DOC_DIR = os.path.join(ROOT_DIR, "doc")
SRC_DIR = os.path.join(ROOT_DIR, "src")

ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.csv")
STUDENT_FILE = os.path.join(DATA_DIR, "student.csv")