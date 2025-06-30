# 🎓 UET Attendance Management System

This is a **Python-based Attendance Management System** for UET students.
It allows you to manage student records, mark daily attendance, generate pie charts, send automatic email notifications for absentees, and much more — all through an interactive, colorful terminal interface!

---

## ✨ Features

✅ Admin login with username and password
✅ Add new students with name & email validation
✅ Remove students by roll number
✅ Mark daily attendance (Present / Absent / Leave)
✅ Send automatic email notifications if a student is absent or on leave
✅ View today’s attendance of all students in a table format
✅ View detailed record of a particular student
✅ Generate pie chart for each student’s attendance
✅ Fully colored, centered terminal UI with UET banner
✅ JSON file to store and manage student records

---

## 🗂️ Project Structure

```
Attendance-Management-System/
│
├── attendence.py      # Main Python program
├── com.json           # Student data file (attendance records)
├── README.md          # This file
├── .gitignore         # (Optional) Ignore system or IDE files
├── requirements.txt   # (Optional) List of required Python packages
```

---

## ⚙️ Requirements

* Python 3.x installed
* Required Python libraries:

  * pandas
  * matplotlib
  * tabulate
  * pyfiglet
  * colorama

✅ Install them using:

```bash
pip install pandas matplotlib tabulate pyfiglet colorama
```

---

## 🚀 How to Run

Clone the repository or download the project folder.

Then run:

```bash
python attendence.py
```

Use the menu to:

* Add student attendance
* View today’s attendance
* View particular student record
* Add or remove students
* Exit the system

---

## 🔐 Admin Credentials

Default credentials:

* **Username:** `admin`
* **Password:** `12345`

✅ You can change these in the `attendence.py` file as needed.

---

## 📁 Data File

* **`com.json`** contains all student details & attendance records.
* This file is automatically updated whenever you add/remove students or mark attendance.
* Keep a backup of this file for safety.

---

## 📧 Email Configuration

The system automatically sends an email if a student is **Absent** or on **Leave**.

To configure:

* Open the `send_email()` function in `attendence.py`.
* Replace with your sender email and app password:

  ```python
  sender_email = "shannaseem06@gmail.com"
  sender_password = "malh fndi wubw loyd"
  ```

✅ Use **app passwords** for Gmail (recommended) — never push real credentials to GitHub!

---

## 🛡️ Security Tips

* Change your admin password regularly.
* Never commit real email passwords or API keys to public repos.
* Keep a backup of `com.json` to avoid data loss.

---

## 🙌 Author

**👤 Shan Naseem**
Python Developer 

---

## ⚡ License

This project is created for educational purposes only.
Feel free to use, modify, and improve it.

---

## 💙 Happy Coding!

If you like this project, star it on GitHub and share your feedback! 🚀✨
