
# ============================================================
# COLLEGE MANAGEMENT & STUDENT PERFORMANCE ANALYTICS SYSTEM
# Main Application
# ============================================================

# STUDENT MANAGEMENT IMPORTS
from modules.student import (
    add_student,
    view_students,
    update_student_email,
    delete_student,
    search_student,
    filter_students_by_course,
    count_students
)

# COURSE AND SUBJECT MANAGEMENT IMPORTS
from modules.course import (
    add_course,
    view_courses,
    update_course,
    delete_course,
    search_courses,
    check_course_dependencies,
    add_subject,
    view_subjects,
    filter_subjects_by_course,
    count_subjects_by_course
)

# ATTENDANCE MANAGEMENT IMPORTS
from modules.attendance import (
    mark_attendance,
    view_attendance,
    update_attendance,
    delete_attendance,
    student_attendance_report,
    attendance_by_date,
    course_attendance_summary
)

# EXAMINATION AND MARKS MANAGEMENT IMPORTS
from modules.examination import (
    add_exam,
    view_exams,
    update_exam,
    delete_exam,
    add_marks,
    view_marks,
    update_marks,
    delete_marks,
    student_result_report,
    subject_result_summary,
    top_performers
)


# ============================================================
# INPUT VALIDATION FUNCTIONS
# ============================================================

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid whole number.")


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


# ============================================================
# 1. STUDENT MANAGEMENT
# ============================================================

def student_menu():

    while True:

        print("\n" + "=" * 45)
        print("          STUDENT MANAGEMENT")
        print("=" * 45)

        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student Email")
        print("4. Delete Student")
        print("5. Search Student")
        print("6. Filter Students by Course")
        print("7. Count Students")
        print("8. Back to Main Menu")

        choice = input("\nEnter your choice (1-8): ")

        if choice == "1":

            name = input("Enter student name: ")
            age = get_int("Enter age: ")
            email = input("Enter email: ")
            course_id = get_int("Enter course ID: ")

            add_student(name, age, email, course_id)

        elif choice == "2":

            view_students()

        elif choice == "3":

            student_id = get_int("Enter student ID: ")
            new_email = input("Enter new email: ")

            update_student_email(student_id, new_email)

        elif choice == "4":

            student_id = get_int("Enter student ID: ")
            delete_student(student_id)

        elif choice == "5":

            keyword = input("Enter student name or keyword: ")
            search_student(keyword)

        elif choice == "6":

            course_name = input("Enter course name: ")
            filter_students_by_course(course_name)

        elif choice == "7":

            count_students()

        elif choice == "8":

            break

        else:

            print("Invalid choice. Please try again.")


# ============================================================
# 2. COURSE MANAGEMENT
# ============================================================

def course_menu():

    while True:

        print("\n" + "=" * 45)
        print("           COURSE MANAGEMENT")
        print("=" * 45)

        print("1. Add Course")
        print("2. View Courses")
        print("3. Update Course")
        print("4. Delete Course")
        print("5. Search Courses")
        print("6. Check Course Dependencies")
        print("7. Back to Main Menu")

        choice = input("\nEnter your choice (1-7): ")

        if choice == "1":

            course_name = input("Enter course name: ")
            duration = get_int("Enter course duration in years: ")

            add_course(course_name, duration)

        elif choice == "2":

            view_courses()

        elif choice == "3":

            course_id = get_int("Enter course ID: ")
            new_name = input("Enter new course name: ")
            new_duration = get_int("Enter new duration in years: ")

            update_course(course_id, new_name, new_duration)

        elif choice == "4":

            course_id = get_int("Enter course ID: ")
            delete_course(course_id)

        elif choice == "5":

            keyword = input("Enter course name or keyword: ")
            search_courses(keyword)

        elif choice == "6":

            course_id = get_int("Enter course ID: ")
            check_course_dependencies(course_id)

        elif choice == "7":

            break

        else:

            print("Invalid choice. Please try again.")


# ============================================================
# 3. SUBJECT MANAGEMENT
# ============================================================

def subject_menu():

    while True:

        print("\n" + "=" * 45)
        print("           SUBJECT MANAGEMENT")
        print("=" * 45)

        print("1. Add Subject")
        print("2. View Subjects")
        print("3. Filter Subjects by Course")
        print("4. Count Subjects by Course")
        print("5. Back to Main Menu")

        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":

            subject_name = input("Enter subject name: ")
            course_id = get_int("Enter course ID: ")

            add_subject(subject_name, course_id)

        elif choice == "2":

            view_subjects()

        elif choice == "3":

            course_name = input("Enter course name: ")
            filter_subjects_by_course(course_name)

        elif choice == "4":

            count_subjects_by_course()

        elif choice == "5":

            break

        else:

            print("Invalid choice. Please try again.")


# ============================================================
# 4. ATTENDANCE MANAGEMENT
# ============================================================

def attendance_menu():

    while True:

        print("\n" + "=" * 45)
        print("          ATTENDANCE MANAGEMENT")
        print("=" * 45)

        print("1. Mark Attendance")
        print("2. View All Attendance")
        print("3. Update Attendance")
        print("4. Delete Attendance")
        print("5. Student Attendance Report")
        print("6. Attendance by Date")
        print("7. Course Attendance Summary")
        print("8. Back to Main Menu")

        choice = input("\nEnter your choice (1-8): ")

        if choice == "1":

            student_id = get_int("Enter student ID: ")
            subject_id = get_int("Enter subject ID: ")
            attendance_date = input("Enter date (YYYY-MM-DD): ")
            status = input("Enter status (Present/Absent): ")

            mark_attendance(
                student_id,
                subject_id,
                attendance_date,
                status
            )

        elif choice == "2":

            view_attendance()

        elif choice == "3":

            attendance_id = get_int("Enter attendance ID: ")
            new_status = input("Enter new status (Present/Absent): ")

            update_attendance(attendance_id, new_status)

        elif choice == "4":

            attendance_id = get_int("Enter attendance ID: ")
            delete_attendance(attendance_id)

        elif choice == "5":

            student_id = get_int("Enter student ID: ")
            student_attendance_report(student_id)

        elif choice == "6":

            attendance_date = input("Enter date (YYYY-MM-DD): ")
            attendance_by_date(attendance_date)

        elif choice == "7":

            course_attendance_summary()

        elif choice == "8":

            break

        else:

            print("Invalid choice. Please try again.")


# ============================================================
# 5. EXAMINATION AND MARKS MANAGEMENT
# ============================================================

def examination_menu():

    while True:

        print("\n" + "=" * 45)
        print("     EXAMINATION & MARKS MANAGEMENT")
        print("=" * 45)

        print("1. Add Examination")
        print("2. View Examinations")
        print("3. Update Examination")
        print("4. Delete Examination")
        print("5. Add Student Marks")
        print("6. View All Marks")
        print("7. Update Marks")
        print("8. Delete Marks")
        print("9. Student Result Report")
        print("10. Subject-wise Result Summary")
        print("11. View Top Performers")
        print("12. Back to Main Menu")

        choice = input("\nEnter your choice (1-12): ")

        if choice == "1":

            subject_id = get_int("Enter subject ID: ")
            exam_name = input("Enter examination name: ")
            max_marks = get_float("Enter maximum marks: ")

            add_exam(subject_id, exam_name, max_marks)

        elif choice == "2":

            view_exams()

        elif choice == "3":

            exam_id = get_int("Enter examination ID: ")
            new_name = input("Enter new examination name: ")
            new_max_marks = get_float("Enter new maximum marks: ")

            update_exam(exam_id, new_name, new_max_marks)

        elif choice == "4":

            exam_id = get_int("Enter examination ID: ")
            delete_exam(exam_id)

        elif choice == "5":

            student_id = get_int("Enter student ID: ")
            exam_id = get_int("Enter examination ID: ")
            marks = get_float("Enter marks obtained: ")

            add_marks(student_id, exam_id, marks)

        elif choice == "6":

            view_marks()

        elif choice == "7":

            mark_id = get_int("Enter marks record ID: ")
            new_marks = get_float("Enter updated marks: ")

            update_marks(mark_id, new_marks)

        elif choice == "8":

            mark_id = get_int("Enter marks record ID: ")
            delete_marks(mark_id)

        elif choice == "9":

            student_id = get_int("Enter student ID: ")
            student_result_report(student_id)

        elif choice == "10":

            exam_id = get_int("Enter examination ID: ")
            subject_result_summary(exam_id)

        elif choice == "11":

            exam_id = get_int("Enter examination ID: ")
            limit = get_int("Enter number of top performers: ")

            top_performers(exam_id, limit)

        elif choice == "12":

            break

        else:

            print("Invalid choice. Please try again.")


# ============================================================
# MAIN APPLICATION MENU
# ============================================================

def main_menu():

    while True:

        print("\n" + "=" * 50)
        print("       COLLEGE MANAGEMENT SYSTEM")
        print("=" * 50)

        print("1. Student Management")
        print("2. Course Management")
        print("3. Subject Management")
        print("4. Attendance Management")
        print("5. Examination & Marks Management")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ")

        if choice == "1":

            student_menu()

        elif choice == "2":

            course_menu()

        elif choice == "3":

            subject_menu()

        elif choice == "4":

            attendance_menu()

        elif choice == "5":

            examination_menu()

        elif choice == "6":

            print("\nThank you for using College Management System.")
            print("Application closed successfully.")
            break

        else:

            print("\nInvalid choice. Please try again.")


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main_menu()
