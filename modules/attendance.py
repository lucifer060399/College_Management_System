
from database.db_connection import get_connection
from datetime import datetime


# ==================================
# ATTENDANCE VALIDATION
# ==================================

def validate_date(attendance_date):
    try:
        datetime.strptime(attendance_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# ==================================
# MARK ATTENDANCE
# ==================================

def mark_attendance(student_id, subject_id, attendance_date, status):

    if not validate_date(attendance_date):
        print("Invalid date! Use YYYY-MM-DD format.")
        return

    status = status.capitalize()

    if status not in ("Present", "Absent"):
        print("Status must be Present or Absent.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Verify that the subject belongs to the student's course
        cursor.execute("""
            SELECT s.student_id
            FROM students s
            JOIN subjects sub
                ON s.course_id = sub.course_id
            WHERE s.student_id = ?
              AND sub.subject_id = ?
        """, (student_id, subject_id))

        if cursor.fetchone() is None:
            print("Student or subject not found, or subject does not belong to student's course.")
            return

        cursor.execute("""
            INSERT INTO attendance
            (student_id, subject_id, attendance_date, status)
            VALUES (?, ?, ?, ?)
        """, (student_id, subject_id, attendance_date, status))

        connection.commit()
        print("Attendance marked successfully!")

    except Exception as error:
        connection.rollback()
        print("Error marking attendance:", error)

    finally:
        connection.close()


# ==================================
# VIEW ALL ATTENDANCE
# ==================================

def view_attendance():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            a.attendance_id,
            s.name,
            sub.subject_name,
            c.course_name,
            a.attendance_date,
            a.status
        FROM attendance a
        JOIN students s
            ON a.student_id = s.student_id
        JOIN subjects sub
            ON a.subject_id = sub.subject_id
        JOIN courses c
            ON s.course_id = c.course_id
        ORDER BY a.attendance_date, s.name
    """)

    records = cursor.fetchall()

    print("\nALL ATTENDANCE RECORDS")

    if records:
        for record in records:
            print(record)
    else:
        print("No attendance records found.")

    connection.close()


# ==================================
# UPDATE ATTENDANCE
# ==================================

def update_attendance(attendance_id, new_status):

    new_status = new_status.capitalize()

    if new_status not in ("Present", "Absent"):
        print("Status must be Present or Absent.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE attendance
            SET status = ?
            WHERE attendance_id = ?
        """, (new_status, attendance_id))

        connection.commit()

        if cursor.rowcount > 0:
            print("Attendance updated successfully!")
        else:
            print("Attendance record not found.")

    except Exception as error:
        connection.rollback()
        print("Error updating attendance:", error)

    finally:
        connection.close()


# ==================================
# DELETE ATTENDANCE
# ==================================

def delete_attendance(attendance_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM attendance
            WHERE attendance_id = ?
        """, (attendance_id,))

        connection.commit()

        if cursor.rowcount > 0:
            print("Attendance record deleted successfully!")
        else:
            print("Attendance record not found.")

    except Exception as error:
        connection.rollback()
        print("Error deleting attendance:", error)

    finally:
        connection.close()


# ==================================
# STUDENT-WISE ATTENDANCE
# ==================================

def student_attendance_report(student_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.student_id,
            s.name,
            sub.subject_name,
            COUNT(a.attendance_id) AS total_classes,
            SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END)
                AS present_classes,
            SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END)
                AS absent_classes,
            ROUND(
                100.0 * SUM(
                    CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END
                ) / NULLIF(COUNT(a.attendance_id), 0),
                2
            ) AS attendance_percentage
        FROM attendance a
        JOIN students s
            ON a.student_id = s.student_id
        JOIN subjects sub
            ON a.subject_id = sub.subject_id
        WHERE s.student_id = ?
        GROUP BY s.student_id, s.name, sub.subject_id, sub.subject_name
        ORDER BY sub.subject_name
    """, (student_id,))

    records = cursor.fetchall()

    print("\nSTUDENT ATTENDANCE REPORT")

    if records:
        for record in records:
            print(record)
    else:
        print("No attendance records found for this student.")

    connection.close()


# ==================================
# DATE-WISE ATTENDANCE
# ==================================

def attendance_by_date(attendance_date):

    if not validate_date(attendance_date):
        print("Invalid date! Use YYYY-MM-DD format.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            s.name,
            sub.subject_name,
            a.status
        FROM attendance a
        JOIN students s
            ON a.student_id = s.student_id
        JOIN subjects sub
            ON a.subject_id = sub.subject_id
        WHERE a.attendance_date = ?
        ORDER BY sub.subject_name, s.name
    """, (attendance_date,))

    records = cursor.fetchall()

    print(f"\nATTENDANCE FOR {attendance_date}")

    if records:
        for record in records:
            print(record)
    else:
        print("No attendance records found for this date.")

    connection.close()


# ==================================
# COURSE-WISE ATTENDANCE SUMMARY
# ==================================

def course_attendance_summary():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.course_name,
            COUNT(a.attendance_id) AS total_records,
            SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END)
                AS present_records,
            SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END)
                AS absent_records,
            ROUND(
                100.0 * SUM(
                    CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END
                ) / NULLIF(COUNT(a.attendance_id), 0),
                2
            ) AS attendance_percentage
        FROM courses c
        LEFT JOIN students s
            ON c.course_id = s.course_id
        LEFT JOIN attendance a
            ON s.student_id = a.student_id
        GROUP BY c.course_id, c.course_name
        ORDER BY c.course_name
    """)

    records = cursor.fetchall()

    print("\nCOURSE-WISE ATTENDANCE SUMMARY")

    for record in records:
        print(record)

    connection.close()
