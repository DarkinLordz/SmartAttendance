from path import FACE_DIR, ATTENDANCE_FILE
from deepface import DeepFace
import database
import cv2
import os

def mark_attendance(student_id):
    import csv
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = datetime.now().strftime("%Y-%m-%d")

    records = []
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            records = list(reader)
            
    for r in records:
        if r["student_id"] == str(student_id) and r["timestamp"].startswith(today):
            return

    file_exists = os.path.exists(ATTENDANCE_FILE)
    with open(ATTENDANCE_FILE, "a", newline="", encoding="utf-8") as file:
        fieldnames = ["student_id", "timestamp"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({"student_id": student_id, "timestamp": timestamp})

def recognize_face():
    students = database.get_all_students()
    
    if not students:
        print("No students enrolled yet.")
        return

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Cannot open camera")
        return

    print("Press 'q' to stop")
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        temp_path = "temp.jpg"
        cv2.imwrite(temp_path, frame)

        for student in students:
            student_face_path = os.path.join(FACE_DIR, student["student_face"])
            if not os.path.exists(student_face_path):
                continue

            try:
                result = DeepFace.verify(img1_path=temp_path, img2_path=student_face_path, enforce_detection=False)
                if result["verified"]:
                    print(f"{student['student_name']} recognized!")
                    mark_attendance(student["student_id"])
            except Exception as e:
                print("Error verifying face:", e)

        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()