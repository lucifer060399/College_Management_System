
from database.db_connection import get_connection


def add_exam(subject_id, exam_name, max_marks):
    """Add an examination for a subject."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        if max_marks <= 0:
            print("Maximum marks must be greater than zero.")
            return

        cursor.execute(
            """
            INSERT INTO examinations (subject_id, exam_name, max_marks)
            VALUES (?, ?, ?)
            """,
            (subject_id, exam_name, max_marks)
        )

        connection.commit()
        print("Examination added successfully.")

    except Exception as error:
        connection.rollback()
        print("Error adding examination:", error)

    finally:
        connection.close()


def view_exams():
    """Display all examinations with their subject and course."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            e.exam_id,
            e.exam_name,
            s.subject_name,
            c.course_name,
            e.max_marks
        FROM examinations e
        JOIN subjects s ON e.subject_id = s.subject_id
        JOIN courses c ON s.course_id = c.course_id
        ORDER BY e.exam_id
        """
    )

    records = cursor.fetchall()
    connection.close()

    for record in records:
        print(record)


def update_exam(exam_id, new_exam_name, new_max_marks):
    """Update examination details."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        if new_max_marks <= 0:
            print("Maximum marks must be greater than zero.")
            return

        cursor.execute(
            """
            UPDATE examinations
            SET exam_name = ?, max_marks = ?
            WHERE exam_id = ?
            """,
            (new_exam_name, new_max_marks, exam_id)
        )

        if cursor.rowcount == 0:
            print("Examination not found.")
        else:
            connection.commit()
            print("Examination updated successfully.")

    except Exception as error:
        connection.rollback()
        print("Error updating examination:", error)

    finally:
        connection.close()


def delete_exam(exam_id):
    """Delete an examination."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM examinations WHERE exam_id = ?",
            (exam_id,)
        )

        if cursor.rowcount == 0:
            print("Examination not found.")
        else:
            connection.commit()
            print("Examination deleted successfully.")

    except Exception as error:
        connection.rollback()
        print("Error deleting examination:", error)

    finally:
        connection.close()


# --------------------------------------------------
# MARKS MANAGEMENT
# --------------------------------------------------

def add_marks(student_id, exam_id, marks_obtained):
    """Enter marks after validating student and examination."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT e.max_marks, s.course_id
            FROM examinations e
            JOIN subjects s ON e.subject_id = s.subject_id
            WHERE e.exam_id = ?
            """,
            (exam_id,)
        )

        exam = cursor.fetchone()

        if exam is None:
            print("Examination not found.")
            return

        max_marks, exam_course_id = exam

        cursor.execute(
            "SELECT course_id FROM students WHERE student_id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            print("Student not found.")
            return

        if student[0] != exam_course_id:
            print("This student does not belong to the examination's course.")
            return

        if marks_obtained < 0 or marks_obtained > max_marks:
            print(f"Marks must be between 0 and {max_marks}.")
            return

        cursor.execute(
            """
            INSERT INTO marks (student_id, exam_id, marks_obtained)
            VALUES (?, ?, ?)
            """,
            (student_id, exam_id, marks_obtained)
        )

        connection.commit()
        print("Marks added successfully.")

    except Exception as error:
        connection.rollback()
        print("Error adding marks:", error)

    finally:
        connection.close()


def view_marks():
    """Display marks with student, examination and subject details."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            m.mark_id,
            st.name,
            e.exam_name,
            s.subject_name,
            m.marks_obtained,
            e.max_marks
        FROM marks m
        JOIN students st ON m.student_id = st.student_id
        JOIN examinations e ON m.exam_id = e.exam_id
        JOIN subjects s ON e.subject_id = s.subject_id
        ORDER BY m.mark_id
        """
    )

    records = cursor.fetchall()
    connection.close()

    for record in records:
        print(record)


def update_marks(mark_id, new_marks):
    """Update marks after validating the maximum marks."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT e.max_marks
            FROM marks m
            JOIN examinations e ON m.exam_id = e.exam_id
            WHERE m.mark_id = ?
            """,
            (mark_id,)
        )

        record = cursor.fetchone()

        if record is None:
            print("Marks record not found.")
            return

        max_marks = record[0]

        if new_marks < 0 or new_marks > max_marks:
            print(f"Marks must be between 0 and {max_marks}.")
            return

        cursor.execute(
            """
            UPDATE marks
            SET marks_obtained = ?
            WHERE mark_id = ?
            """,
            (new_marks, mark_id)
        )

        connection.commit()
        print("Marks updated successfully.")

    except Exception as error:
        connection.rollback()
        print("Error updating marks:", error)

    finally:
        connection.close()


def delete_marks(mark_id):
    """Delete a marks record."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM marks WHERE mark_id = ?",
            (mark_id,)
        )

        if cursor.rowcount == 0:
            print("Marks record not found.")
        else:
            connection.commit()
            print("Marks record deleted successfully.")

    except Exception as error:
        connection.rollback()
        print("Error deleting marks:", error)

    finally:
        connection.close()


# --------------------------------------------------
# RESULT AND PERFORMANCE REPORTS
# --------------------------------------------------

def calculate_grade(percentage):
    """Calculate grade using the sample project grading scale."""

    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def student_result_report(student_id):
    """Display a student's examination results."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            st.name,
            s.subject_name,
            e.exam_name,
            m.marks_obtained,
            e.max_marks
        FROM marks m
        JOIN students st ON m.student_id = st.student_id
        JOIN examinations e ON m.exam_id = e.exam_id
        JOIN subjects s ON e.subject_id = s.subject_id
        WHERE st.student_id = ?
        ORDER BY s.subject_name, e.exam_name
        """,
        (student_id,)
    )

    records = cursor.fetchall()
    connection.close()

    if not records:
        print("No examination results found for this student.")
        return

    print("\nSTUDENT RESULT REPORT")
    print("-" * 65)

    for name, subject, exam, obtained, maximum in records:
        percentage = (obtained / maximum) * 100
        grade = calculate_grade(percentage)

        print(
            f"{name} | {subject} | {exam} | "
            f"{obtained}/{maximum} | {percentage:.2f}% | Grade: {grade}"
        )


def subject_result_summary(exam_id):
    """Display student results for a particular examination."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            st.student_id,
            st.name,
            m.marks_obtained,
            e.max_marks
        FROM marks m
        JOIN students st ON m.student_id = st.student_id
        JOIN examinations e ON m.exam_id = e.exam_id
        WHERE e.exam_id = ?
        ORDER BY m.marks_obtained DESC
        """,
        (exam_id,)
    )

    records = cursor.fetchall()
    connection.close()

    if not records:
        print("No marks found for this examination.")
        return

    print("\nEXAMINATION RESULT SUMMARY")
    print("-" * 65)

    for student_id, name, obtained, maximum in records:
        percentage = (obtained / maximum) * 100
        grade = calculate_grade(percentage)

        print(
            f"{student_id} | {name} | "
            f"{obtained}/{maximum} | {percentage:.2f}% | {grade}"
        )


def top_performers(exam_id, limit=3):
    """Display the highest scoring students in an examination."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            st.student_id,
            st.name,
            m.marks_obtained,
            e.max_marks,
            ROUND((m.marks_obtained * 100.0 / e.max_marks), 2)
                AS percentage
        FROM marks m
        JOIN students st ON m.student_id = st.student_id
        JOIN examinations e ON m.exam_id = e.exam_id
        WHERE e.exam_id = ?
        ORDER BY percentage DESC, st.student_id
        LIMIT ?
        """,
        (exam_id, limit)
    )

    records = cursor.fetchall()
    connection.close()

    if not records:
        print("No results available for this examination.")
        return

    print("\nTOP PERFORMERS")
    print("-" * 50)

    for position, record in enumerate(records, start=1):
        print(position, record)
