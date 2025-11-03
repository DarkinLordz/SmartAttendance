from path import STUDENTS_CSV, ATTENDANCE_CSV
import time
import csv
import os
from log import logger

def timestamp():
    t = time.strftime("%Y/%m/%d/%H/%M/%S", time.localtime())
    logger.debug(f"Generated timestamp: {t}")
    return t

def get_all_students():
    logger.debug("Fetching all students from CSV")
    if not os.path.exists(STUDENTS_CSV):
        logger.warning(f"Students CSV not found: {STUDENTS_CSV}")
        return []
    with open(STUDENTS_CSV, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        students = [{"student_id": int(row["student_id"]), 
                     "student_name": row["student_name"], 
                     "student_class": row["student_class"], 
                     "student_face": row["student_face"]} for row in reader]
        logger.info(f"Loaded {len(students)} students")
        return students

def generate_student_id():
    students = get_all_students()
    new_id = 1 if not students else max(s["student_id"] for s in students) + 1
    logger.debug(f"Generated new student ID: {new_id}")
    return new_id

def mark_attendance(student, logged_today):
    logger.debug(f"Marking attendance for student: {student['student_id']}")
    if student["student_id"] in logged_today:
        logger.info(f"Student {student['student_id']} already logged today")
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
    logger.info(f"Attendance marked for student: {student['student_id']}")

def write_absent_students(all_students, logged_today):
    logger.debug("Writing absent students")
    file_exists = os.path.exists(ATTENDANCE_CSV)
    with open(ATTENDANCE_CSV, "a", newline="", encoding="utf-8") as file:
        fieldnames = ["student_id", "student_name", "student_class", "student_time"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        absent = [s for s in all_students if s["student_id"] not in logged_today]
        writer.writerows({
            "student_id": s["student_id"],
            "student_name": s["student_name"],
            "student_class": s.get("student_class", ""),
            "student_time": ""
        } for s in absent)
    logger.info(f"Wrote {len(absent)} absent students")

def add_student(student_id, student_name, student_class, student_face):
    logger.debug(f"Adding student: {student_id}, {student_name}")
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
    logger.info(f"Student added: {student_id}, {student_name}")

def remove_student(student_id):
    logger.debug(f"Removing student: {student_id}")
    student_id = int(student_id)
    students = [s for s in get_all_students() if s['student_id'] != student_id]
    with open(STUDENTS_CSV, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["student_id", "student_name", "student_class", "student_face"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)
    logger.info(f"Student removed: {student_id}")