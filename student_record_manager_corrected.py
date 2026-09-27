import re
import os

# Find files in the same folder as this Python file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "input.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "students.txt")


def validate_student(roll_no, name, email, age):
    """
    Check each field and return the exact invalid field message.
    Returns None when all fields are valid.
    """

    # Roll Number
    if not roll_no.isdigit():
        return "INVALID ROLL NUMBER"

    # Name
    if not name.strip() or not re.fullmatch(r"[A-Za-z ]+", name):
        return "INVALID NAME"

    # Email
    email_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
    if not re.fullmatch(email_pattern, email):
        return "INVALID EMAIL"

    # Age
    if not age.isdigit() or not 1 <= int(age) <= 100:
        return "INVALID AGE"

    return None


def read_input_file():
    """Read input.txt and separate valid and invalid records."""

    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()

    except FileNotFoundError:
        print("ERROR: input.txt file not found.")
        print("Keep input.txt in the same folder as this Python file.")
        return [], 0

    valid_students = []
    invalid_count = 0
    record_number = 0

    print("\n===== RECORD VALIDATION =====\n")

    for line in lines:
        line = line.strip()

        if not line:
            continue

        record_number += 1

        parts = line.split("|")

        # Check record format first
        if len(parts) != 4:
            invalid_count += 1
            print(f"Record {record_number}: INVALID")
            print("INVALID FORMAT")
            print(f"Data: {line}")
            print("-" * 45)
            continue

        roll_no, name, email, age = [
            item.strip() for item in parts
        ]

        error = validate_student(
            roll_no, name, email, age
        )

        if error:
            invalid_count += 1

            print(f"Record {record_number}: INVALID")
            print(error)
            print(f"Data: {line}")
            print("-" * 45)

        else:
            valid_students.append(
                (roll_no, name, email, age)
            )

            print(f"Record {record_number}: VALID")
            print(f"Name : {name}")
            print(f"Email: {email}")
            print(f"Age  : {age}")
            print("-" * 45)

    return valid_students, invalid_count


def save_students(students):
    """Save only valid student records."""

    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

            for roll_no, name, email, age in students:
                file.write(
                    f"{roll_no}|{name}|{email}|{age}\n"
                )

        print("\nValid student records saved to students.txt.")

    except OSError as error:
        print("Error while saving file:", error)


def display_students():
    """Display the records saved in students.txt."""

    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
            records = file.readlines()

        print("\n===== SAVED STUDENT RECORDS =====")

        if not records:
            print("No valid records saved.")
            return

        for line in records:
            roll_no, name, email, age = line.strip().split("|")

            print(
                f"Roll Number: {roll_no} | "
                f"Name: {name} | "
                f"Email: {email} | "
                f"Age: {age}"
            )

    except FileNotFoundError:
        print("students.txt not found.")


def main():
    print("======================================")
    print("       STUDENT RECORD MANAGER")
    print("======================================")

    valid_students, invalid_count = read_input_file()

    print("\n===== SUMMARY =====")
    print(f"Valid Records   : {len(valid_students)}")
    print(f"Invalid Records : {invalid_count}")

    if valid_students:
        save_students(valid_students)
        display_students()
    else:
        print("\nNo valid records to save.")


if __name__ == "__main__":
    main()
