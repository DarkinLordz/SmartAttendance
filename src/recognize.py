from path import FACES_DIR, RECOGNIZE_WAV
from deepface import DeepFace
import database
import sound
import numpy
import cv2
import os
import time
from log import logger

def load_student_embeddings():
    logger.debug("Loading student embeddings")
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
                    logger.info(f"Loaded embedding for {img_path}")
                except Exception as e:
                    logger.error(f"Failed to load embedding for {img_path}: {e}")
                    continue
        embeddings.append({
            "student_id": student["student_id"],
            "student_name": student["student_name"],
            "student_class": student.get("student_class", ""),
            "embeddings": student_embeds
        })
    logger.debug(f"Loaded embeddings for {len(embeddings)} students")
    return embeddings

def is_match(embedding1, embedding2, threshold=0.70):
    cos_sim = numpy.dot(embedding1, embedding2.T) / (numpy.linalg.norm(embedding1) * numpy.linalg.norm(embedding2))
    logger.debug(f"Cosine similarity: {cos_sim}, threshold: {threshold}")
    return cos_sim >= threshold

def recognize_face():
    logger.info("Starting face recognition")
    student_data = load_student_embeddings()
    if not student_data:
        logger.warning("No student data found")
        return

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        logger.error("Cannot open camera")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    logged_today = set()
    check_interval = 24 * 60 * 60
    next_check = time.time() + check_interval

    while True:
        if time.time() >= next_check:
            logger.info("Writing absent students and resetting log for the day")
            database.write_absent_students(student_data, logged_today)
            logged_today.clear()
            next_check = time.time() + check_interval

        ret, frame = cam.read()
        if not ret:
            logger.warning("Failed to read frame from camera")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        logger.debug(f"Detected {len(faces)} faces")

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_img = frame[y:y+h, x:x+w]

            try:
                face_embed = DeepFace.represent(
                    img_path=face_img,
                    model_name='ArcFace',
                    detector_backend='opencv',
                    enforce_detection=True
                )
                frame_embedding = numpy.array(face_embed[0]["embedding"])
                logger.debug("Face embedding generated for detected face")
            except Exception as e:
                logger.error(f"Failed to generate embedding for detected face: {e}")
                continue

            for student in student_data:
                if student["student_id"] in logged_today:
                    continue
                if any(is_match(frame_embedding, embed) for embed in student["embeddings"]):
                    logger.info(f"Recognized student: {student['student_id']} - {student['student_name']}")
                    database.mark_attendance(student, logged_today)
                    try:
                        sound.play(RECOGNIZE_WAV)
                    except Exception as e:
                        logger.error(f"Failed to play recognition sound: {e}")
        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.info("Quitting face recognition loop")
            break

    cam.release()
    cv2.destroyAllWindows()
    logger.info("Camera released and windows destroyed")

if __name__ == "__main__":
    recognize_face()