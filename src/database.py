from path import STUDENTS_CSV, ATTENDANCE_CSV
import time
import csv
import os

def timestamp():
    return time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())

def get_all_students():
    if not os.path.exists(STUDENTS_CSV):
        return []
    with open(STUDENTS_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [{"student_id": int(row["student_id"]), 
                 "student_name": row["student_name"], 
                 "student_class": row["student_class"], 
                 "student_face": row["student_face"]} for row in reader]

def generate_student_id():
    students = get_all_students()
    return 1 if not students else max(s["student_id"] for s in students) + 1

def mark_attendance(student, logged_today):
    if student["student_id"] in logged_today:
        return
    file_exists = os.path.exists(ATTENDANCE_CSV)
    with open(ATTENDANCE_CSV, "a", newline="", encoding="utf-8") as file:
        fieldnames = ["student_id", "student_name", "student_class", "student_time"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "student_id": student["student_id"],
            "student_name": student["student_name"],
            "student_class": student.get("student_class", ""),
            "student_time": timestamp()
        })
    logged_today.add(student["student_id"])

def write_absent_students(all_students, logged_today):
    file_exists = os.path.exists(ATTENDANCE_CSV)
    with open(ATTENDANCE_CSV, "a", newline="", encoding="utf-8") as file:
        fieldnames = ["student_id", "student_name", "student_class", "student_time"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows({
            "student_id": s["student_id"],
            "student_name": s["student_name"],
            "student_class": s.get("student_class", ""),
            "student_time": ""
        } for s in all_students if s["student_id"] not in logged_today)

def add_student(student_id, student_name, student_class, student_face):
    file_exists = os.path.exists(STUDENTS_CSV)
    with open(STUDENTS_CSV, "a", newline="", encoding="utf-8") as file:
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
    with open(STUDENTS_CSV, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["student_id", "student_name", "student_class", "student_face"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)