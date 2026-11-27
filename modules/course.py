
from database.db_connection import get_connection


# ==============================
# COURSE MANAGEMENT
# ==============================

def add_course(course_name, duration):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO courses (course_name, duration)
            VALUES (?, ?)
        """, (course_name, duration))

        connection.commit()
        print("Course added successfully!")

    except Exception as error:
        connection.rollback()
        print("Error adding course:", error)

    finally:
        connection.close()


def view_courses():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.course_id,
            c.course_name,
            c.duration,
            COUNT(s.student_id) AS total_students
        FROM courses c
        LEFT JOIN students s
            ON c.course_id = s.course_id
        GROUP BY c.course_id, c.course_name, c.duration
        ORDER BY c.course_id
    """)

    courses = cursor.fetchall()

    print("\nCOURSE DETAILS")
    for course in courses:
        print(course)

    connection.close()


def update_course(course_id, new_name, new_duration):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE courses
            SET course_name = ?, duration = ?
            WHERE course_id = ?
        """, (new_name, new_duration, course_id))

        connection.commit()

        if cursor.rowcount > 0:
            print("Course updated successfully!")
        else:
            print("Course ID not found.")

    except Exception as error:
        connection.rollback()
        print("Error updating course:", error)

    finally:
        connection.close()


def delete_course(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM courses
            WHERE course_id = ?
        """, (course_id,))

        connection.commit()

        if cursor.rowcount > 0:
            print("Course deleted successfully!")
        else:
            print("Course ID not found.")

    except Exception as error:
        connection.rollback()
        print("Cannot delete course:", error)

    finally:
        connection.close()


# ==============================
# SUBJECT MANAGEMENT
# ==============================

def add_subject(subject_name, course_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO subjects (subject_name, course_id)
            VALUES (?, ?)
        """, (subject_name, course_id))

        connection.commit()
        print("Subject added successfully!")

    except Exception as error:
        connection.rollback()
        print("Error adding subject:", error)

    finally:
        connection.close()


def view_subjects():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.subject_id,
            s.subject_name,
            c.course_name
        FROM subjects s
        INNER JOIN courses c
            ON s.course_id = c.course_id
        ORDER BY c.course_name, s.subject_name
    """)

    subjects = cursor.fetchall()

    print("\nSUBJECT DETAILS")
    for subject in subjects:
        print(subject)

    connection.close()


def filter_subjects_by_course(course_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.subject_id,
            s.subject_name,
            c.course_name
        FROM subjects s
        INNER JOIN courses c
            ON s.course_id = c.course_id
        WHERE c.course_name = ?
    """, (course_name,))

    subjects = cursor.fetchall()

    print(f"\nSUBJECTS FOR {course_name}")
    for subject in subjects:
        print(subject)

    connection.close()


def count_subjects_by_course():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.course_name,
            COUNT(s.subject_id) AS total_subjects
        FROM courses c
        LEFT JOIN subjects s
            ON c.course_id = s.course_id
        GROUP BY c.course_id, c.course_name
        ORDER BY c.course_name
    """)

    results = cursor.fetchall()

    print("\nSUBJECT COUNT BY COURSE")
    for result in results:
        print(result)

    connection.close()


def search_courses(keyword):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT course_id, course_name, duration
        FROM courses
        WHERE course_name LIKE ?
        ORDER BY course_name
    """, (f"%{keyword}%",))

    results = cursor.fetchall()

    print("\nCOURSE SEARCH RESULTS")
    for course in results:
        print(course)

    connection.close()


def check_course_dependencies(course_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            (SELECT COUNT(*) FROM students
             WHERE course_id = ?),
            (SELECT COUNT(*) FROM subjects
             WHERE course_id = ?)
    """, (course_id, course_id))

    students, subjects = cursor.fetchone()

    print("Students associated:", students)
    print("Subjects associated:", subjects)

    connection.close()
