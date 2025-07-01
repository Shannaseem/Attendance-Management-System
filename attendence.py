import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import pandas as pd
import json
import os
from datetime import date
from tabulate import tabulate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyfiglet
import msvcrt
import shutil
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add at the top if not already:
from shutil import get_terminal_size

# GLOBAL COLORS FOR ALL TEXT
DEFAULT_COLOR = Fore.CYAN
HEADER_COLOR = Fore.YELLOW
ERROR_COLOR = Fore.RED
SUCCESS_COLOR = Fore.GREEN
INPUT_COLOR = Fore.MAGENTA
TITLE_COLOR = Fore.BLUE

# Banner
# Banner
def show_uet_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    terminal_width = shutil.get_terminal_size().columns

    # Join words into one string
    banner_text = pyfiglet.figlet_format("UET   ATTENDENCE   SYSTEM", font="big", width=1000)

    for line in banner_text.splitlines():
        print(Fore.MAGENTA	 + Style.BRIGHT + line.center(terminal_width))


# Centered print
def cprint(text="", color=DEFAULT_COLOR, style=Style.BRIGHT, end="\n", flush=False):
    width = shutil.get_terminal_size().columns
    print(color + style + text.center(width), end=end, flush=flush)

# Centered input
def cinput(prompt, color=INPUT_COLOR, style=Style.BRIGHT):
    width = shutil.get_terminal_size().columns
    full_prompt = prompt + " "
    prompt_x = (width - len(full_prompt)) // 2
    print(" " * prompt_x + color + style + full_prompt, end="", flush=True)

    user_input = ""
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:
            print()
            break
        elif ch == b'\x08':
            if user_input:
                user_input = user_input[:-1]
                print("\b \b", end="", flush=True)
        elif ch == b' ':
            continue
        else:
            decoded = ch.decode()
            user_input += decoded
            print(color + style + decoded, end="", flush=True)
    return user_input

# Constants
TOTAL_DAYS = 30

# Add attendance
def add_attendance_and_show_chart():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen first
    show_uet_banner()
    json_path = r"D:\\Phython\\ATTENDENCE SYSTEM\\com.json"

    cprint("You are Taking Attendance of Class")

    try:
        with open(json_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        cprint(" File not found.\n", ERROR_COLOR)
        return
    except json.JSONDecodeError:
        cprint(" Invalid JSON format.\n", ERROR_COLOR)
        return

    cprint(f"\nTotal Students of Class: {len(data['students'])}\n", SUCCESS_COLOR)
    subject = "Com"
    att_date = str(date.today())

    for student in data["students"]:
        cprint(f"\nRoll: {student['roll']} | Name: {student['name']}\n", HEADER_COLOR)
        student.setdefault("attendance", {}).setdefault(subject, {})

        while True:
            status = cinput("Enter (P=Present, A=Absent, L=Leave) [Default: P]: ").strip().upper()
            if status == "":
                status = "P"
                break
            elif status in ["P", "A", "L"]:
                break
            else:
                cprint("  Invalid input! Please enter P, A, or L only.", ERROR_COLOR)

        student["attendance"][subject][att_date] = status

        # 👉 Send email if Absent or Leave
        if status in ["A", "L"]:
            recipient_email = student.get("email")
            if recipient_email:
                email_sent = send_email(
                    "user@example.com",  # Replace with your sender email
                    "myourpassword",      # Replace with your app password
                    recipient_email,
                    f"Attendance Status for {student['name']}",
                    f"Dear {student['name']},\n\nYou have been marked as '{status}' for subject {subject} on {att_date}.\n\nRegards,\nAdmin"
                )
                if email_sent:
                    cprint(f" ✅ Email has been sent to {student['name']} at {recipient_email}\n", SUCCESS_COLOR)
                else:
                    cprint(f" ❌ Failed to send email to {student['name']}\n", ERROR_COLOR)
            else:
                cprint(f" ⚠️ No email found for {student['name']}. Cannot send email.\n", ERROR_COLOR)

        show_student_pie_chart(student, subject)

    # Save updated data
    try:
        with open(json_path, "w") as file:
            json.dump(data, file, indent=4)
        cprint("\n ✅ All attendance saved successfully.\n", SUCCESS_COLOR)

        while True:
            tell = cinput("Enter 1 to show Menu list or 0 to Exit: ").strip()
            if tell == "1":
                menu()
                break
            elif tell == "0":
                cprint("\n You are exiting the program.", ERROR_COLOR)
                exit()
            else:
                cprint(" Invalid input! Please enter 1 or 0.", ERROR_COLOR)

    except Exception as e:
        cprint(f" Error saving file: {e}\n", ERROR_COLOR)


# Pie chart
def show_student_pie_chart(student, subject):
    name = student["name"]
    attendance_data = student.get("attendance", {}).get(subject, {})
    counts = {"P": 0, "A": 0, "L": 0}
    for status in attendance_data.values():
        if status in counts:
            counts[status] += 1
    recorded = sum(counts.values())
    remaining = TOTAL_DAYS - recorded

    labels, values, colors = [], [], []

    if counts["P"] > 0:
        labels.append("Present")
        values.append(counts["P"])
        colors.append("#4CAF50")

    if counts["A"] > 0:
        labels.append("Absent")
        values.append(counts["A"])
        colors.append("#F44336")  # Red

    if counts["L"] > 0:
        labels.append("Leave")
        values.append(counts["L"])
        colors.append("#FFC107")  # Amber

    if remaining > 0:
        labels.append("Remaining")
        values.append(remaining)
        colors.append("#B0BEC5")  # Grey

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
    plt.title(f"{name}'s {subject} Attendance ({TOTAL_DAYS} Days)")
    plt.axis("equal")
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(0.1)

    cprint(f"\n{name}'s chart is open. Press ENTER to close and continue...", INPUT_COLOR)
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:
            break
    plt.close()

# Show table
def show_today_attendance_table():
    json_path = r"D:\\Phython\\ATTENDENCE SYSTEM\\com.json"
    subject = "Com"
    today = str(date.today())
    os.system('cls' if os.name == 'nt' else 'clear')  # clear screen first
    show_uet_banner()

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        cprint(" File not found.\n", ERROR_COLOR)
        return
    except json.JSONDecodeError:
        cprint(" Invalid JSON format.\n", ERROR_COLOR)
        return
    if "students" not in data or not data["students"]:
        cprint(" No students found in the file.\n", ERROR_COLOR)
        return

    records = [[s.get("roll", ""), s.get("name", ""), s.get("attendance", {}).get(subject, {}).get(today, "Not Marked")] for s in data["students"]]
    headers = ["Roll", "Name", "Status"]
    table = tabulate(records, headers=headers, tablefmt="fancy_grid", colalign=["center"] * len(headers))
    cprint(f"\n Attendance Table for Subject: {subject} | Date: {today}\n", HEADER_COLOR)


    # When showing the table:
    term_width = get_terminal_size().columns

    cprint('\n'.join([line.center(term_width) for line in table.splitlines()]))
    cprint()
    while True:
            tell = cinput("Enter 1 to show Menu list or 0 to Exit: ").strip()
            if tell == "1":
                menu()
                break
            elif tell == "0":
                cprint("\n You are exiting the program.", ERROR_COLOR)
                exit()
            else:
                cprint(" Invalid input! Please enter 1 or 0.", ERROR_COLOR)

# Send email
def send_email(sender_email, sender_password, recipient_email, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        return True   # ✅ Email sent successfully
    except Exception as e:
        cprint(f"Error sending email: {str(e)}\n", ERROR_COLOR)
        return False  # ❌ Email failed
    
from datetime import datetime
def show_particular_student_attendance():
    os.system('cls' if os.name == 'nt' else 'clear')
    show_uet_banner()

    json_path = r"D:\\Phython\\ATTENDENCE SYSTEM\\com.json"
    subject = "Com"

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        cprint(" File not found.\n", ERROR_COLOR)
        return
    except json.JSONDecodeError:
        cprint(" Invalid JSON format.\n", ERROR_COLOR)
        return

    if "students" not in data or not data["students"]:
        cprint()
        cprint(" No students found in the file.\n", ERROR_COLOR)
        return

    while True:
        cprint()
        roll_number = cinput("Enter Roll Number of Student: ").strip()

        student = next((s for s in data["students"] if s.get("roll") == roll_number), None)

        if not student:
            cprint()
            cprint(f" ❌ No student found with roll number: {roll_number}\n", ERROR_COLOR)

            # Keep asking until Y/N is valid
            while True:
                try_again = cinput("Do you want to try again? (Y/N): ").strip().upper()
                if try_again in ["Y", "N"]:
                    break
                else:
                    cprint(" Invalid input! Please enter Y or N only.", ERROR_COLOR)

            if try_again == "Y":
                continue  # Try again
            else:
                while True:
                    tell = cinput("Enter 1 to show Menu list or 0 to Exit: ").strip()
                    if tell == "1":
                        menu()
                        return
                    elif tell == "0":
                        cprint("\n You are exiting the program.", ERROR_COLOR)
                        exit()
                    else:
                        cprint(" Invalid input! Please enter 1 or 0.", ERROR_COLOR)
                return
        else:
            break  # Student found, exit while loop

    # ✅ Show student info
    cprint(f"\nAttendance Record for: {student['name']} (Roll: {student['roll']})\n", HEADER_COLOR)
    email = student.get("email", "N/A")
    cprint(f"Email: {email}\n", SUCCESS_COLOR)

    attendance_records = student.get("attendance", {}).get(subject, {})

    if not attendance_records:
        cprint(" No attendance records found.\n", ERROR_COLOR)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')  # clear screen first
        show_uet_banner()
        cprint(f"\nAttendance Record for: {student['name']} (Roll: {student['roll']})\n", HEADER_COLOR)

        table_data = []
        counts = {"P": 0, "A": 0, "L": 0}

        for date, status in sorted(attendance_records.items()):
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                day_name = date_obj.strftime("%A")
            except:
                day_name = "-"
            table_data.append([date, day_name, status, subject])

            if status in counts:
                counts[status] += 1

        headers = ["Date", "Day", "Status", "Subject"]

        table = tabulate(table_data, headers=headers, tablefmt="fancy_grid", colalign=["center"]*len(headers))

        term_width = get_terminal_size().columns
        cprint('\n'.join([line.center(term_width) for line in table.splitlines()]))

        total_days = sum(counts.values())
        percent_present = (counts["P"] / total_days) * 100 if total_days else 0
        summary = f"Total: {total_days} | Present: {counts['P']} | Absent: {counts['A']} | Leave: {counts['L']} | % Present: {percent_present:.2f}%"
        cprint(f"\n{summary}\n", SUCCESS_COLOR)

    # ✅ Ask for pie chart
    while True:
        ask_chart = cinput("\nDo you want to view the pie chart for this student? (Y/N): ").strip().upper()
        if ask_chart == "Y":
            show_student_pie_chart(student, subject)
            break
        elif ask_chart == "N":
            break
        else:
            cprint(" Invalid input! Please enter Y or N.", ERROR_COLOR)

    # ✅ Final menu options
    cprint()
    while True:
        tell = cinput("Enter 1 to show Menu list or 0 to Exit: ").strip()
        if tell == "1":
            menu()
            break
        elif tell == "0":
            cprint("\n You are exiting the program.", ERROR_COLOR)
            exit()
        else:
            cprint(" Invalid input! Please enter 1 or 0.", ERROR_COLOR)
import re  # ✅ Required for pattern matching

def add_student_to_attendance_system():
    os.system('cls' if os.name == 'nt' else 'clear')
    show_uet_banner()

    json_path = r"D:\\Phython\\ATTENDENCE SYSTEM\\com.json"

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        cprint(" File not found.\n", ERROR_COLOR)
        return
    except json.JSONDecodeError:
        cprint(" Invalid JSON format.\n", ERROR_COLOR)
        return

    students = data.get("students", [])

    # ✅ Find next roll number
    if students:
        try:
            last_roll = max(int(s.get("roll", 0)) for s in students)
        except ValueError:
            last_roll = 100
    else:
        last_roll = 100

    new_roll = str(last_roll + 1)

    cprint(f"\nAssigning Roll Number: {new_roll}\n", HEADER_COLOR)

    # ✅ Input validation for Name
    while True:
        name = cinput("Enter Student Name : ").strip()
        if not name:
            cprint(" Name cannot be empty!", ERROR_COLOR)
            continue
        if not re.match(r'^[A-Za-z ]+$', name):
            cprint(" Invalid name! Only letters and spaces allowed.", ERROR_COLOR)
            continue
        break

    # ✅ Input validation for Email
    while True:
        email = cinput("Enter Student Email : ").strip()
        if not email:
            cprint(" Email cannot be empty!", ERROR_COLOR)
            continue
        # Basic email pattern: text@text.domain
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            cprint(" Invalid email format! Example: someone@example.com", ERROR_COLOR)
            continue
        break

    new_student = {
        "roll": new_roll,
        "name": name,
        "email": email,
        "attendance": {}
    }

    students.append(new_student)
    data["students"] = students

    try:
        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)
        os.system('cls' if os.name == 'nt' else 'clear')  # clear screen first
        show_uet_banner()
        cprint(f"\n  Student added successfully!\n Roll: {new_roll}\n Name: {name}\n Email: {email}\n", SUCCESS_COLOR)
    except Exception as e:
        cprint(f" Error saving file: {e}\n", ERROR_COLOR)

    while True:
        tell = cinput("Enter 1 to show Menu list or 0 to Exit: ").strip()
        if tell == "1":
            menu()
            break
        elif tell == "0":
            cprint("\n You are exiting the program.", ERROR_COLOR)
            exit()
        else:
            cprint(" Invalid input! Please enter 1 or 0.", ERROR_COLOR)


def remove_student_from_attendance_system():
    os.system('cls' if os.name == 'nt' else 'clear')
    show_uet_banner()

    json_path = r"D:\\Phython\\ATTENDENCE SYSTEM\\com.json"

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        cprint(" File not found.\n", ERROR_COLOR)
        return
    except json.JSONDecodeError:
        cprint(" Invalid JSON format.\n", ERROR_COLOR)
        return

    students = data.get("students", [])

    if not students:
        cprint("\n No students found in the system.\n", ERROR_COLOR)
        return

    while True:
        cprint()
        roll_number = cinput("Enter Roll Number of Student to Remove: ").strip()

        index_to_remove = None
        for idx, student in enumerate(students):
            if student.get("roll") == roll_number:
                index_to_remove = idx
                found_student = student
                break

        if index_to_remove is None:
            cprint()
            cprint(f" ❌ No student found with roll number: {roll_number}\n", ERROR_COLOR)
            try_again = cinput("Do you want to try again? (Y/N): ").strip().upper()
            while try_again not in ["Y", "N"]:
                cprint(" Invalid input! Please enter Y or N.", ERROR_COLOR)
                try_again = cinput("Do you want to try again? (Y/N): ").strip().upper()
            if try_again == "Y":
                continue
            else:
                break
        else:
            cprint(f"\nFound Student: {found_student['name']} (Roll: {found_student['roll']})\n", SUCCESS_COLOR)
            confirm = cinput("Are you sure you want to remove this student? (Y/N): ").strip().upper()
            while confirm not in ["Y", "N"]:
                cprint(" Invalid input! Please enter Y or N.", ERROR_COLOR)
                confirm = cinput("Are you sure you want to remove this student? (Y/N): ").strip().upper()

            if confirm == "Y":
                del students[index_to_remove]
                data["students"] = students  # Update the list

                try:
                    with open(json_path, "w") as f:
                        json.dump(data, f, indent=4)
                    cprint(f"\n ✅ Student {found_student['name']} (Roll: {found_student['roll']}) removed successfully!\n", SUCCESS_COLOR)
                except Exception as e:
                    cprint(f" Error saving file: {e}\n", ERROR_COLOR)
                break
            else:
                cprint("\n Student not removed.\n", ERROR_COLOR)
                break

    while True:
        tell = cinput("Enter 1 to show Menu list or 0 to Exit: ").strip()
        if tell == "1":
            menu()
            break
        elif tell == "0":
            cprint("\n You are exiting the program.", ERROR_COLOR)
            exit()
        else:
            cprint(" Invalid input! Please enter 1 or 0.", ERROR_COLOR)


# Password input
def input_password():
    width = shutil.get_terminal_size().columns
    prompt = "Enter Admin Password : "
    left_padding = (width - len(prompt)) // 2
    print(INPUT_COLOR + Style.BRIGHT + " " * left_padding + prompt, end="", flush=True)
    pwd = ""
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:
            print()
            return pwd
        elif ch == b'\x08':
            if pwd:
                pwd = pwd[:-1]
        elif ch == b" ":
            continue
        elif len(pwd) < 12:
            try:
                char = ch.decode()
                pwd += char
            except:
                continue

# Admin name input
def input_admin_name():
    width = shutil.get_terminal_size().columns
    prompt = "Enter   Admin   Name : "
    left_padding = (width - len(prompt)) // 2
    print(INPUT_COLOR + Style.BRIGHT + " " * left_padding + prompt, end="", flush=True)
    name = ""
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:
            print()
            return name
        elif ch == b'\x08':
            if name:
                name = name[:-1]
                print("\b \b", end="", flush=True)
        elif ch == b" ":
            continue
        elif len(name) < 12:
            try:
                char = ch.decode()
                name += char
            except:
                continue

# Menu


def menu():

    cprint()
    os.system('cls' if os.name == 'nt' else 'clear')  # clear screen first
    show_uet_banner()
    cprint("======STUDENT ATTENDENCE MANAGEMENT SYSTEM======", HEADER_COLOR)
    cprint()
    cprint("1: ADD ATTENDENCE OF STUDENTS\n")
    cprint("2: VIEW ATTENDENCE OF ALL STUDENTS\n")
    cprint("3: VIEW ATTENDENCE OF PARTICULAR STUDENTS\n")
    cprint("4: ADD STUDENTS TO ATTENDENCE SYSTEM\n")
    cprint("5: REMOVE STUDENT FROM ATTENDENCE SYSTEM\n")
    cprint("6: EXIT FROM ATTENDENCE SYSTEM\n")
    while True:
        ask = cinput(" Enter your choice from the above menu : ")
        match ask:
            case "1":
                add_attendance_and_show_chart()
            case "2":
                show_today_attendance_table()
            case "3":
                show_particular_student_attendance()
            case "4":
                add_student_to_attendance_system()
            case "5":
                remove_student_from_attendance_system()
            case "6":
                cprint("\n Exiting the Attendance System. Have a great day ahead!\n", SUCCESS_COLOR)
                exit()
            case _:
                cprint("Kindly choose the choice from 1 to 6\n", ERROR_COLOR)

# Main Execution
if __name__ == "__main__":
    show_uet_banner()
    correct_name = "admin"
    correct_password = "12345"
    attempts = 0
    max_attempts = 3
    cprint("====== Admin Login ======", HEADER_COLOR)
    while attempts < max_attempts:
        cprint()
        admin_name = input_admin_name()
        admin_pass = input_password()
        if admin_name == correct_name and admin_pass == correct_password:
            cprint()
            os.system('cls' if os.name == 'nt' else 'clear')  # clear screen first
            show_uet_banner()

            cprint(f" Welcome ! You are now logged in.\n", SUCCESS_COLOR)
            cprint()
            while True:
                tell = cinput("Enter 1 to show Menu list or 0 to Exit: ").strip()
                if tell == "1":
                    menu()
                    break
                elif tell == "0":
                    cprint("\n You are exiting the program.", ERROR_COLOR)
                    exit()
                else:
                    cprint(" Invalid input! Please enter 1 or 0.", ERROR_COLOR)
        else:
            attempts += 1
            cprint(f" Invalid credentials. Attempts left: {max_attempts - attempts}\n", ERROR_COLOR)
    if attempts == max_attempts:
        cprint(" Too many failed attempts. Exiting program.\n", ERROR_COLOR)
