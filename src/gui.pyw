import customtkinter as ctk
import database
from log import logger

class SmartAttendance(ctk.CTk):

    def __init__(self):
        super().__init__()
        logger.info("SmartAttendance GUI started")
        self.title("SmartAttendance")
        self.geometry("500x300")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.add_frame = ctk.CTkFrame(self, corner_radius=12)
        self.add_frame.pack(pady=10, fill="x", padx=20)

        self.name_entry = ctk.CTkEntry(self.add_frame, placeholder_text="Student Name")
        self.name_entry.pack(pady=5, padx=10, fill="x")

        self.class_entry = ctk.CTkEntry(self.add_frame, placeholder_text="Student Class")
        self.class_entry.pack(pady=5, padx=10, fill="x")

        self.face_entry = ctk.CTkEntry(self.add_frame, placeholder_text="Face File Name")
        self.face_entry.pack(pady=5, padx=10, fill="x")

        self.add_button = ctk.CTkButton(self.add_frame, text="Add Student", command=self.add_student)
        self.add_button.pack(pady=10)

        self.remove_frame = ctk.CTkFrame(self, corner_radius=12)
        self.remove_frame.pack(pady=10, fill="x", padx=20)

        self.remove_id_entry = ctk.CTkEntry(self.remove_frame, placeholder_text="Student ID to Remove")
        self.remove_id_entry.pack(pady=5, padx=10, fill="x")

        self.remove_button = ctk.CTkButton(self.remove_frame, text="Remove Student", fg_color="red", command=self.remove_student)
        self.remove_button.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="", text_color="lightgreen", font=("Arial", 13))
        self.status_label.pack(pady=10)

    def add_student(self):
        name = self.name_entry.get().strip()
        sclass = self.class_entry.get().strip()
        face = self.face_entry.get().strip()

        logger.debug(f"Add student requested: name={name}, class={sclass}, face={face}")

        if not name or not sclass or not face:
            self.status_label.configure(text="Please fill all fields.", text_color="red")
            logger.warning("Add student failed: missing fields")
            return

        student_id = database.generate_student_id()
        database.add_student(student_id, name, sclass, face)
        self.status_label.configure(text=f"Student added successfully! ID: {student_id}", text_color="lightgreen")
        logger.info(f"Student added via GUI: {student_id}, {name}")

        self.name_entry.delete(0, "end")
        self.class_entry.delete(0, "end")
        self.face_entry.delete(0, "end")

    def remove_student(self):
        student_id = self.remove_id_entry.get().strip()
        logger.debug(f"Remove student requested: id={student_id}")
        if not student_id:
            self.status_label.configure(text="Please enter a student ID.", text_color="red")
            logger.warning("Remove student failed: missing ID")
            return

        database.remove_student(student_id)
        self.status_label.configure(text=f"Removed student with ID: {student_id}", text_color="orange")
        logger.info(f"Student removed via GUI: {student_id}")

        self.remove_id_entry.delete(0, "end")

if __name__ == "__main__":
    app = SmartAttendance()
    app.mainloop()