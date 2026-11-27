
from database.db_connection import get_connection


def insert_courses():
    connection = get_connection()
    cursor = connection.cursor()

    courses = [
        ("BCA", 3),
        ("BSc Computer Science", 3),
        ("BCom", 3),
        ("MCA", 2),
        ("MSc Computer Science", 2)
    ]

    try:
        cursor.executemany(
            """
            INSERT INTO courses (course_name, duration)
            VALUES (?, ?)
            """,
            courses
        )

        connection.commit()
        print("Sample courses inserted successfully!")

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    insert_courses()
