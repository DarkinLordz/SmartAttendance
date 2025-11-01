from path import FACES_DIR, RECOGNIZE_WAV
from deepface import DeepFace
import database
import sound
import numpy
import cv2
import os
import time

def load_student_embeddings():
    students = database.get_all_students()
    embeddings = []
    for student in students:
        student_images = student["student_face"]
        student_embeds = []
        for img_name in student_images if isinstance(student_images, list) else [student_images]:
            img_path = os.path.join(FACES_DIR, img_name)
            if os.path.exists(img_path):
                try:
                    embed = DeepFace.represent(img_path=img_path, model_name='ArcFace', enforce_detection=True)
                    student_embeds.append(numpy.array(embed[0]["embedding"]))
                except Exception:
                    continue
        embeddings.append({
            "student_id": student["student_id"],
            "student_name": student["student_name"],
            "student_class": student.get("student_class", ""),
            "embeddings": student_embeds
        })
    return embeddings

def is_match(embedding1, embedding2, threshold=0.70):
    cos_sim = numpy.dot(embedding1, embedding2.T) / (numpy.linalg.norm(embedding1) * numpy.linalg.norm(embedding2))
    return cos_sim >= threshold

def recognize_face():
    student_data = load_student_embeddings()
    if not student_data:
        return

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Cannot open camera")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    logged_today = set()
    check_interval = 24 * 60 * 60
    next_check = time.time() + check_interval

    while True:
        if time.time() >= next_check:
            database.write_absent_students(student_data, logged_today)
            logged_today.clear()
            next_check = time.time() + check_interval

        ret, frame = cam.read()
        if not ret:
            continue

        cv2.imshow("Camera", frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]

            try:
                face_embed = DeepFace.represent(
                    img_path=face_img,
                    model_name='ArcFace',
                    detector_backend='opencv',
                    enforce_detection=True
                )
                frame_embedding = numpy.array(face_embed[0]["embedding"])
            except Exception:
                continue

            for student in student_data:
                if student["student_id"] in logged_today:
                    continue
                if any(is_match(frame_embedding, embed) for embed in student["embeddings"]):
                    database.mark_attendance(student, logged_today)
                    try:
                        sound.play(RECOGNIZE_WAV)
                    except:
                        pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_face()