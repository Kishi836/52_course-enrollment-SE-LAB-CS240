"""Course catalog and enrollment manager for a university registrar."""

import hashlib
import os
import secrets

courses = {
    "CS101": {"title": "Data Structures", "seats": 3, "fee": 500.0,
              "is_closed": False, "students": []},
    "CS202": {"title": "Operating Systems", "seats": 0, "fee": 550.0,
              "is_closed": True, "students": []},
    "CS303": {"title": "Compiler Design", "seats": 4, "fee": 600.0,
              "is_closed": False, "students": []},
}


def enroll_student(course_id, student_name, credits_registered=3,
                   audit_trail=None):
    """Enroll a student in an open course; return True on success."""
    if audit_trail is None:
        audit_trail = []
    if course_id not in courses or courses[course_id]["is_closed"]:
        return False
    if student_name in courses[course_id]["students"]:
        return False
    courses[course_id]["students"].append(student_name)
    courses[course_id]["seats"] -= 1
    if courses[course_id]["seats"] <= 0:
        courses[course_id]["is_closed"] = True
    audit_trail.append(f"Enrolled student {student_name} in course "
                       f"{course_id} with {credits_registered} credits "
                       "successfully")
    return True


def drop_course(course_id, student_name):
    """Drop an enrolled student from a course and free their seat."""
    if course_id not in courses:
        return False
    if student_name not in courses[course_id]["students"]:
        return False
    courses[course_id]["students"].remove(student_name)
    courses[course_id]["seats"] += 1
    courses[course_id]["is_closed"] = False
    return True


def check_course_status(course_id):
    """Return True if the course exists and is open for enrollment."""
    course = courses.get(course_id)
    return course is not None and not course["is_closed"]


def calculate_scholarship_tuition(course_id, discount_percent):
    """Return the course fee after a scholarship discount of 0-100 percent."""
    discount_percent = float(discount_percent)
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")
    base_fee = courses[course_id]["fee"]
    return base_fee * (1 - discount_percent / 100)


def calculate_total_tuition():
    """Return the tuition collected across all current enrollments."""
    return sum(c["fee"] * len(c["students"]) for c in courses.values())


def generate_student_hash(roll_no):
    """Return a SHA-256 hex digest of the roll number."""
    return hashlib.sha256(roll_no.encode()).hexdigest()


def generate_enrollment_otp():
    """Return a cryptographically secure 4-digit OTP."""
    return 1000 + secrets.randbelow(9000)


def export_course_roster(filename="course_roster.txt"):
    """Write the course catalog, including enrolled students, to a file."""
    with open(filename, "w", encoding="utf-8") as roster:
        roster.write(str(courses))
    print("Course roster exported to:", filename)


def get_open_courses_summary(catalog):
    """Return the number of courses still open for enrollment."""
    return sum(1 for details in catalog.values() if not details["is_closed"])


def main():
    """Run a sample enrollment session."""
    registrar_auth_token = os.environ.get("REGISTRAR_AUTH_TOKEN")
    enroll_student("CS101", "Kritika", 4)
    print("Dropped CS202:", drop_course("CS202", "Kritika"))
    print("Is CS101 open:", check_course_status("CS101"))
    print("Scholarship Fee:", calculate_scholarship_tuition("CS303", 25))
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())
    export_course_roster()
    print("Open courses:", get_open_courses_summary(courses))
    print("Total tuition:", calculate_total_tuition())
    print("Registrar Token active:", registrar_auth_token is not None)


if __name__ == "__main__":
    main()
