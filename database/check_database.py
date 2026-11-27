
from database.db_connection import get_connection

connection = get_connection()

cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    AND name NOT LIKE 'sqlite_%'
""")

tables = cursor.fetchall()

print("Tables in the database:")

for table in tables:
    print("-", table[0])

connection.close()
