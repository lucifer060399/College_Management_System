
from database.db_connection import get_connection


def add_student(name, age, email, course_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO students (name, age, email, course_id)
            VALUES (?, ?, ?, ?)
            """,
            (name, age, email, course_id)
        )

        connection.commit()
        print("Student registered successfully!")

    except Exception as error:
        connection.rollback()
        print("Error registering student:", error)

    finally:
        connection.close()


def view_students():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.student_id,
            s.name,
            s.age,
            s.email,
            c.course_name
        FROM students s
        JOIN courses c
            ON s.course_id = c.course_id
        ORDER BY s.student_id
    """)

    students = cursor.fetchall()

    for student in students:
        print(student)

    connection.close()


def update_student_email(student_id, new_email):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE students
            SET email = ?
            WHERE student_id = ?
            """,
            (new_email, student_id)
        )

        connection.commit()

        if cursor.rowcount > 0:
            print("Student email updated successfully!")
        else:
            print("Student ID not found.")

    except Exception as error:
        connection.rollback()
        print("Error updating student:", error)

    finally:
        connection.close()


def delete_student(student_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )

        connection.commit()

        if cursor.rowcount > 0:
            print("Student deleted successfully!")
        else:
            print("Student ID not found.")

    except Exception as error:
        connection.rollback()
        print("Error deleting student:", error)

    finally:
        connection.close()


def search_student(keyword):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT s.student_id, s.name, s.age, s.email, c.course_name
        FROM students s
        JOIN courses c ON s.course_id = c.course_id
        WHERE s.name LIKE ?
        ORDER BY s.name
    """, (f"%{keyword}%",))

    results = cursor.fetchall()

    if results:
        for student in results:
            print(student)
    else:
        print("No students found.")

    connection.close()


def filter_students_by_course(course_name):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT s.student_id, s.name, s.age, s.email, c.course_name
        FROM students s
        JOIN courses c ON s.course_id = c.course_id
        WHERE c.course_name = ?
    """, (course_name,))

    results = cursor.fetchall()

    for student in results:
        print(student)

    connection.close()


def count_students():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")

    count = cursor.fetchone()[0]

    print("Total students:", count)

    connection.close()
