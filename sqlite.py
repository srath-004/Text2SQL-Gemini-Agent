import sqlite3

conn = sqlite3.connect("student.db")
cur = conn.cursor()

# Remove the old table so re-running never creates duplicates
cur.execute("DROP TABLE IF EXISTS STUDENT")

cur.execute("""
CREATE TABLE STUDENT(
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
)
""")

cur.executemany("INSERT INTO STUDENT VALUES(?,?,?,?)", [
    ("Krish", "Data Science", "A", 90),
    ("Sudhanshu", "Data Science", "B", 100),
    ("Darius", "Data Science", "A", 86),
    ("Vikash", "DEVOPS", "A", 50),
    ("Dipesh", "DEVOPS", "A", 35),
])

conn.commit()

# Print the rows so you can confirm the data
print("Rows in STUDENT table:")
for row in cur.execute("SELECT * FROM STUDENT"):
    print(row)

conn.close()