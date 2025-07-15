import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST","localhost")
db_port = os.getenv("DB_PORT","3306")
db_name = os.getenv("DB_NAME")

connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    port=db_port
)

cursor = connection.cursor()

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
cursor.execute(f"USE {db_name}")
table_info = """
create table If Not Exists Student(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT)
"""
cursor.execute(table_info)

## insert records
cursor.execute(table_info)
cursor.execute("TRUNCATE TABLE Student")
# Insert records
records = [
    ("Devansh", "Data Science", "A", 90),
    ("Jai", "Web Development", "B", 95),
    ("Archit", "Web Development", "B", 100),
    ("Sparsh", "Data Science", "A", 95),
    ("Krish", "Data Science", "A", 100)
]

cursor.executemany("INSERT INTO Student VALUES (%s, %s, %s, %s)",records)

# Display the records

print("The inserted records are")
cursor.execute("""Select * From Student""")
data = cursor.fetchall()
for row in data:
    print(row)

# Commit your changes in the database
connection.commit()
connection.close()