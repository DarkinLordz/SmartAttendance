import recognize
import database
import sys

def main():
    if len(sys.argv) < 2:
        return
    command = sys.argv[1]
    if command == "add":
        student_id = database.generate_student_id()
        student_name = input("Enter student name: ")
        student_class = input("Enter student class: ")
        student_face = input("Enter student face file name: ")
        database.add_student(student_id, student_name, student_class, student_face)
    elif command == "remove":
        student_id = input("Enter student id: ")
        database.remove_student(student_id)
    elif command == "start":
        recognize.recognize_face()

if __name__ == "__main__":
    main()