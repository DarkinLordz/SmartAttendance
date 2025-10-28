import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_DIR = os.path.join(ROOT_DIR, "media")
DATA_DIR = os.path.join(ROOT_DIR, "data")
FACE_DIR = os.path.join(DATA_DIR, "face")
SRC_DIR = os.path.join(ROOT_DIR, "src")

ATTENDANCE_CSV = os.path.join(DATA_DIR, "attendance.csv")
STUDENT_CSV = os.path.join(DATA_DIR, "student.csv")

RECOGNIZE_WAV = os.path.join(MEDIA_DIR, "recognize.wav")