# SmartAttendance

**SmartAttendance** is an AI-powered school attendance system designed to automatically detect and recognize students using facial recognition. It aims to make attendance tracking faster, more reliable, and fully digital, reducing manual errors and administrative workload.

---

## **Features**

- **Real-time face recognition**: Detects and identifies students as they enter the classroom.
- **Automated attendance logging**: Marks attendance in the local database automatically.
- **Student database management**: Add, remove, and update student information and facial data.
- **High reliability**: Works best when students pause in front of the camera for accurate recognition.

---

## **Getting Started**

### **Prerequisites**
- Python 3.8+
- Libraries:
  ```bash
  pip install -r requirements.txt
  ```

### **Commands**
- Add:
  ```bash
  python src/main.py add
  ```
- Remove:
  ```bash
  python src/main.py remove
  ```
- Start:
  ```bash
  python src/main.py start
  ```

---

## **How It Works**

Start by adding students to your local database.
When you run the program for the first time, It will install an offline AI model called "ArcFace"
Start by adding students to your database by commands shown above.
Make sure all pictures of students you add are inside "data/face/"
Once done, check your local database in "data/student.csv"
Start the program using commands shown above.
The program will keep the attendance database forever unless you delete it manually.
The database will write absent students in the end of the day. You may know wether a student was absent or not by checking if they have "student_time" row empty. If so, the student was absent for the day.