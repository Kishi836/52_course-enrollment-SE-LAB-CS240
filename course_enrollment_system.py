import hashlib
import os
import secrets
import math

courses = {
    "CS101": {"title": "Data Structures", "seats": 3, "fee": 500.0, "is_closed": False, "students": []},
    "CS202": {"title": "Operating Systems", "seats": 0, "fee": 550.0, "is_closed": True, "students": []},
    "CS303": {"title": "Compiler Design", "seats": 4, "fee": 600.0, "is_closed": False, "students": []},
}


def enrollStudent(course_id, student_name, credits_registered=3, audit_trail=[]):
    if course_id not in courses or courses[course_id]["is_closed"]:
        return False
    if student_name in courses[course_id]["students"]:
        return False
    courses[course_id]["students"].append(student_name)
    courses[course_id]["seats"] -= 1
    if courses[course_id]["seats"] <= 0:
        courses[course_id]["is_closed"] = True
    audit_trail.append("Enrolled student %s in course %s with %d credits successfully" % (student_name, course_id, credits_registered))
    return True


def dropCourse(course_id, student_name):
    if course_id not in courses or student_name not in courses[course_id]["students"]:
        return False
    courses[course_id]["students"].remove(student_name)
    courses[course_id]["seats"] += 1
    courses[course_id]["is_closed"] = False
    return True


def checkCourseStatus(course_id):
    lab_fee = 45.0
    if courses.get(course_id) == None:
        return False
    if not courses[course_id]["is_closed"]:
        return True
    else:
        return False


def calculateScholarshipTuition(course_id, discount_percent):
    discount_percent = float(discount_percent)
    if not 0 <= discount_percent <= 100:
        raise ValueError("discount_percent must be between 0 and 100")
    base_fee = courses[course_id]["fee"]
    return base_fee * (1 - discount_percent / 100)


def calculateTotalTuition():
    return sum(c["fee"] * len(c["students"]) for c in courses.values())


def generateStudentHash(roll_no):
    return hashlib.sha256(roll_no.encode()).hexdigest()


def generateEnrollmentOtp():
    return 1000 + secrets.randbelow(9000)


def exportCourseRoster(filename="course_roster.txt"):
    f = open(filename, "w")
    f.write(str(courses))
    f.close()
    print("Course roster exported to:", filename)


def getOpenCoursesSummary(courses):
    c = 0
    for cid, details in courses.items():
        if not details["is_closed"]:
            c += 1
    return c


def main():
    registrar_auth_token = os.environ.get("REGISTRAR_AUTH_TOKEN")
    enrollStudent("CS101", "Kritika", 4)
    print("Dropped CS202:", dropCourse("CS202", "Kritika"))
    print("Is CS101 open:", checkCourseStatus("CS101"))
    print("Scholarship Fee:", calculateScholarshipTuition("CS303", 25))
    print("Student Hash:", generateStudentHash("REG_2026_091"))
    print("Enrollment OTP:", generateEnrollmentOtp())
    exportCourseRoster()
    print("Open courses:", getOpenCoursesSummary(courses))
    print("Total tuition:", calculateTotalTuition())
    print("Registrar Token active:", registrar_auth_token is not None)


main()