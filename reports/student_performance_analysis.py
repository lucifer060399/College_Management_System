
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from database.db_connection import get_connection


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
EXPORT_DIR = BASE_DIR / "exports"

EXPORT_DIR.mkdir(exist_ok=True)


# ==========================================================
# 1. LOAD DATA FROM SQLITE DATABASE
# ==========================================================

def load_student_data():

    connection = get_connection()

    students_query = """
        SELECT
            s.student_id,
            s.name AS student_name,
            s.age,
            s.email,
            c.course_name
        FROM students s
        JOIN courses c
            ON s.course_id = c.course_id
        ORDER BY s.student_id
    """

    marks_query = """
        SELECT
            s.student_id,
            s.name AS student_name,
            c.course_name,
            sub.subject_name,
            e.exam_name,
            m.marks_obtained,
            e.max_marks,
            ROUND(
                (m.marks_obtained * 100.0) / e.max_marks,
                2
            ) AS percentage
        FROM marks m
        JOIN students s
            ON m.student_id = s.student_id
        JOIN examinations e
            ON m.exam_id = e.exam_id
        JOIN subjects sub
            ON e.subject_id = sub.subject_id
        JOIN courses c
            ON s.course_id = c.course_id
        ORDER BY s.student_id
    """

    attendance_query = """
        SELECT
            s.student_id,
            s.name AS student_name,
            c.course_name,
            sub.subject_name,
            a.attendance_date,
            a.status
        FROM attendance a
        JOIN students s
            ON a.student_id = s.student_id
        JOIN subjects sub
            ON a.subject_id = sub.subject_id
        JOIN courses c
            ON s.course_id = c.course_id
        ORDER BY s.student_id
    """

    try:
        students_df = pd.read_sql_query(
            students_query, connection
        )

        marks_df = pd.read_sql_query(
            marks_query, connection
        )

        attendance_df = pd.read_sql_query(
            attendance_query, connection
        )

    finally:
        connection.close()

    return students_df, marks_df, attendance_df


# ==========================================================
# 2. STUDENT PERFORMANCE ANALYSIS
# ==========================================================

def calculate_grade(percentage):

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


def student_performance_analysis(marks_df):

    if marks_df.empty:
        print("\nNo examination marks available.")
        return pd.DataFrame()

    performance_df = (
        marks_df.groupby(
            ["student_id", "student_name", "course_name"]
        )
        .agg(
            total_exams=("percentage", "count"),
            total_marks=("marks_obtained", "sum"),
            maximum_marks=("max_marks", "sum"),
            average_percentage=("percentage", "mean"),
            highest_percentage=("percentage", "max"),
            lowest_percentage=("percentage", "min")
        )
        .reset_index()
    )

    performance_df["average_percentage"] = (
        performance_df["average_percentage"].round(2)
    )

    performance_df["grade"] = (
        performance_df["average_percentage"]
        .apply(calculate_grade)
    )

    performance_df = performance_df.sort_values(
        by="average_percentage",
        ascending=False
    )

    print("\nSTUDENT PERFORMANCE ANALYSIS")
    print("=" * 100)
    print(performance_df.to_string(index=False))

    return performance_df


# ==========================================================
# 3. SUBJECT-WISE PERFORMANCE ANALYSIS
# ==========================================================

def subject_performance_analysis(marks_df):

    if marks_df.empty:
        print("\nNo subject marks available.")
        return pd.DataFrame()

    subject_df = (
        marks_df.groupby(
            ["course_name", "subject_name"]
        )
        .agg(
            students_appeared=("student_id", "nunique"),
            total_attempts=("percentage", "count"),
            average_percentage=("percentage", "mean"),
            highest_percentage=("percentage", "max"),
            lowest_percentage=("percentage", "min")
        )
        .reset_index()
    )

    subject_df["average_percentage"] = (
        subject_df["average_percentage"].round(2)
    )

    subject_df = subject_df.sort_values(
        by="average_percentage",
        ascending=False
    )

    print("\nSUBJECT-WISE PERFORMANCE ANALYSIS")
    print("=" * 100)
    print(subject_df.to_string(index=False))

    return subject_df


# ==========================================================
# 4. COURSE-WISE PERFORMANCE ANALYSIS
# ==========================================================

def course_performance_analysis(marks_df):

    if marks_df.empty:
        print("\nNo course performance data available.")
        return pd.DataFrame()

    course_df = (
        marks_df.groupby("course_name")
        .agg(
            students_appeared=("student_id", "nunique"),
            total_exams=("percentage", "count"),
            average_percentage=("percentage", "mean"),
            highest_percentage=("percentage", "max")
        )
        .reset_index()
    )

    course_df["average_percentage"] = (
        course_df["average_percentage"].round(2)
    )

    course_df = course_df.sort_values(
        by="average_percentage",
        ascending=False
    )

    print("\nCOURSE-WISE PERFORMANCE ANALYSIS")
    print("=" * 100)
    print(course_df.to_string(index=False))

    return course_df


# ==========================================================
# 5. STUDENT ATTENDANCE ANALYSIS
# ==========================================================

def student_attendance_analysis(attendance_df):

    if attendance_df.empty:
        print("\nNo attendance records available.")
        return pd.DataFrame()

    attendance_summary = (
        attendance_df.groupby(
            ["student_id", "student_name", "course_name"]
        )
        .agg(
            total_classes=("status", "count"),
            present_classes=(
                "status",
                lambda x: (x == "Present").sum()
            ),
            absent_classes=(
                "status",
                lambda x: (x == "Absent").sum()
            )
        )
        .reset_index()
    )

    attendance_summary["attendance_percentage"] = (
        attendance_summary["present_classes"]
        / attendance_summary["total_classes"]
        * 100
    ).round(2)

    attendance_summary["attendance_status"] = (
        attendance_summary["attendance_percentage"]
        .apply(
            lambda x: "Low Attendance" if x < 75 else "Regular"
        )
    )

    print("\nSTUDENT ATTENDANCE ANALYSIS")
    print("=" * 100)
    print(attendance_summary.to_string(index=False))

    return attendance_summary


# ==========================================================
# 6. COURSE-WISE ATTENDANCE ANALYSIS
# ==========================================================

def course_attendance_analysis(attendance_df):

    if attendance_df.empty:
        print("\nNo course attendance data available.")
        return pd.DataFrame()

    course_attendance = (
        attendance_df.groupby("course_name")
        .agg(
            total_records=("status", "count"),
            present_count=(
                "status",
                lambda x: (x == "Present").sum()
            ),
            absent_count=(
                "status",
                lambda x: (x == "Absent").sum()
            )
        )
        .reset_index()
    )

    course_attendance["attendance_percentage"] = (
        course_attendance["present_count"]
        / course_attendance["total_records"]
        * 100
    ).round(2)

    print("\nCOURSE-WISE ATTENDANCE ANALYSIS")
    print("=" * 100)
    print(course_attendance.to_string(index=False))

    return course_attendance


# ==========================================================
# 7. TOP 10 STUDENT PERFORMERS
# ==========================================================

def top_performers_analysis(performance_df):

    if performance_df.empty:
        print("\nNo performance data available.")
        return pd.DataFrame()

    top_students = performance_df.nlargest(
        10, "average_percentage"
    )

    print("\nTOP 10 STUDENT PERFORMERS")
    print("=" * 100)
    print(top_students.to_string(index=False))

    return top_students


# ==========================================================
# 8. EXPORT ANALYTICS TO CSV
# ==========================================================

def export_reports(reports):

    for filename, dataframe in reports.items():

        if dataframe is not None and not dataframe.empty:

            file_path = EXPORT_DIR / filename

            dataframe.to_csv(
                file_path,
                index=False
            )

            print(f"Exported: {file_path}")


# ==========================================================
# 9. VISUALIZATION - STUDENT PERFORMANCE
# ==========================================================

def plot_student_performance(performance_df):

    if performance_df.empty:
        return

    top_students = performance_df.nlargest(
        10, "average_percentage"
    )

    plt.figure(figsize=(12, 6))

    plt.bar(
        top_students["student_name"],
        top_students["average_percentage"]
    )

    plt.title("Top 10 Student Performance")
    plt.xlabel("Student Name")
    plt.ylabel("Average Percentage")
    plt.ylim(0, 100)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(
        EXPORT_DIR / "student_performance.png"
    )

    plt.show()
    plt.close()


# ==========================================================
# 10. VISUALIZATION - SUBJECT PERFORMANCE
# ==========================================================

def plot_subject_performance(subject_df):

    if subject_df.empty:
        return

    plt.figure(figsize=(10, 6))

    plt.bar(
        subject_df["subject_name"],
        subject_df["average_percentage"]
    )

    plt.title("Subject-Wise Average Performance")
    plt.xlabel("Subject")
    plt.ylabel("Average Percentage")
    plt.ylim(0, 100)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(
        EXPORT_DIR / "subject_performance.png"
    )

    plt.show()
    plt.close()


# ==========================================================
# 11. VISUALIZATION - COURSE PERFORMANCE
# ==========================================================

def plot_course_performance(course_df):

    if course_df.empty:
        return

    plt.figure(figsize=(10, 6))

    plt.bar(
        course_df["course_name"],
        course_df["average_percentage"]
    )

    plt.title("Course-Wise Average Performance")
    plt.xlabel("Course")
    plt.ylabel("Average Percentage")
    plt.ylim(0, 100)

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    plt.savefig(
        EXPORT_DIR / "course_performance.png"
    )

    plt.show()
    plt.close()


# ==========================================================
# 12. VISUALIZATION - ATTENDANCE
# ==========================================================

def plot_course_attendance(course_attendance):

    if course_attendance.empty:
        return

    plt.figure(figsize=(10, 6))

    plt.bar(
        course_attendance["course_name"],
        course_attendance["attendance_percentage"]
    )

    plt.axhline(
        y=75,
        linestyle="--",
        label="75% Attendance Reference"
    )

    plt.title("Course-Wise Attendance Percentage")
    plt.xlabel("Course")
    plt.ylabel("Attendance Percentage")
    plt.ylim(0, 100)

    plt.xticks(rotation=30, ha="right")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        EXPORT_DIR / "course_attendance.png"
    )

    plt.show()
    plt.close()


# ==========================================================
# 13. MAIN ANALYTICS PROGRAM
# ==========================================================

def main():

    print("\n")
    print("=" * 65)
    print("       COLLEGE MANAGEMENT SYSTEM")
    print("       STUDENT PERFORMANCE ANALYTICS")
    print("=" * 65)

    print("\nLoading data from SQLite database...")

    students_df, marks_df, attendance_df = (
        load_student_data()
    )

    print("\nDATA LOADING SUMMARY")
    print("-" * 50)

    print("Total Students:", len(students_df))
    print("Total Marks Records:", len(marks_df))
    print("Total Attendance Records:", len(attendance_df))

    # Student performance
    performance_df = student_performance_analysis(
        marks_df
    )

    # Subject performance
    subject_df = subject_performance_analysis(
        marks_df
    )

    # Course performance
    course_df = course_performance_analysis(
        marks_df
    )

    # Student attendance
    student_attendance_df = student_attendance_analysis(
        attendance_df
    )

    # Course attendance
    course_attendance_df = course_attendance_analysis(
        attendance_df
    )

    # Top performers
    top_students_df = top_performers_analysis(
        performance_df
    )

    # Export CSV reports
    reports = {
        "student_performance.csv": performance_df,
        "subject_performance.csv": subject_df,
        "course_performance.csv": course_df,
        "student_attendance.csv": student_attendance_df,
        "course_attendance.csv": course_attendance_df,
        "top_performers.csv": top_students_df
    }

    print("\nEXPORTING REPORTS")
    print("-" * 50)

    export_reports(reports)

    # Generate charts
    print("\nGENERATING CHARTS")
    print("-" * 50)

    plot_student_performance(performance_df)
    plot_subject_performance(subject_df)
    plot_course_performance(course_df)
    plot_course_attendance(course_attendance_df)

    print("\n" + "=" * 65)
    print("ANALYTICS COMPLETED SUCCESSFULLY")
    print("CSV reports and charts are saved in the exports folder.")
    print("=" * 65)


if __name__ == "__main__":
    main()
