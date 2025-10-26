from path import ATTENDANCE_FILE, STUDENT_FILE, FACE_DIR
import csv
import os
import time

def timestamp():
    return time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())

def get_all_students():
    if not os.path.exists(STUDENT_FILE):
        return []
    with open(STUDENT_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [{"student_id": int(row["student_id"]), 
                 "student_name": row["student_name"], 
                 "student_class": row["student_class"], 
                 "student_face": row["student_face"]} for row in reader]

def generate_student_id():
    students = get_all_students()
    return 1 if not students else max(s["student_id"] for s in students) + 1

def add_student(student_id, student_name, student_class, student_face):
    file_exists = os.path.exists(STUDENT_FILE)
    with open(STUDENT_FILE, "a", newline="", encoding="utf-8") as file:
        fieldnames = ["student_id", "student_name", "student_class", "student_face"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "student_id": student_id,
            "student_name": student_name,
            "student_class": student_class,
            "student_face": student_face
        })

def remove_student(student_id):
    student_id = int(student_id)
    students = [s for s in get_all_students() if s['student_id'] != student_id]
    with open(STUDENT_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["student_id", "student_name", "student_class", "student_face"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)