import os
import cv2
import csv
from datetime import datetime, date
from deepface import DeepFace
import numpy as np
import database
from path import FACE_DIR, ATTENDANCE_FILE

def load_student_embeddings():
    students = database.get_all_students()
    embeddings = []
    for student in students:
        student_images = student["student_face"]
        student_embeds = []
        for img_name in student_images if isinstance(student_images, list) else [student_images]:
            img_path = os.path.join(FACE_DIR, img_name)
            if os.path.exists(img_path):
                try:
                    embed = DeepFace.represent(img_path=img_path, model_name='ArcFace', enforce_detection=True)
                    student_embeds.append(np.array(embed[0]["embedding"]))
                except Exception:
                    continue
        embeddings.append({
            "student_id": student["student_id"],
            "student_name": student["student_name"],
            "student_class": student.get("student_class", ""),
            "embeddings": student_embeds
        })
    return embeddings

def mark_attendance(student, logged_today):
    if student["student_id"] in logged_today:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_exists = os.path.exists(ATTENDANCE_FILE)
    with open(ATTENDANCE_FILE, "a", newline="", encoding="utf-8") as file:
        fieldnames = ["student_id", "student_name", "student_class", "student_time"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "student_id": student["student_id"],
            "student_name": student["student_name"],
            "student_class": student.get("student_class", ""),
            "student_time": timestamp
        })
    logged_today.add(student["student_id"])

def is_match(embedding1, embedding2, threshold=0.35):
    cos_sim = np.dot(embedding1, embedding2.T) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return cos_sim > (1 - threshold)

def write_absent_students(all_students, logged_today):
    file_exists = os.path.exists(ATTENDANCE_FILE)
    with open(ATTENDANCE_FILE, "a", newline="", encoding="utf-8") as file:
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

def recognize_face_24_7():
    student_data = load_student_embeddings()
    if not student_data:
        return
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        return
    logged_today = set()
    frame_count = 0
    current_day = date.today()
    while True:
        if date.today() != current_day:
            write_absent_students(student_data, logged_today)
            logged_today.clear()
            current_day = date.today()
        ret, frame = cam.read()
        if not ret:
            continue
        frame_count += 1
        if frame_count % 3 != 0:
            continue
        try:
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            face_embed = DeepFace.represent(img_path=small_frame, model_name='ArcFace', detector_backend='opencv', enforce_detection=True)
            frame_embedding = np.array(face_embed[0]["embedding"])
        except Exception:
            continue
        for student in student_data:
            if student["student_id"] in logged_today:
                continue
            if any(is_match(frame_embedding, embed) for embed in student["embeddings"]):
                mark_attendance(student, logged_today)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()