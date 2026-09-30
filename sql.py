import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("student.db")

# Create a cursor object
cursor = connection.cursor()

# Create Table
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""

# Execute SQL query
cursor.execute(table_info)

# Save changes
connection.commit()

print("STUDENT table created successfully!")


##Insert Some more records 

cursor.execute('''INSERT INTO STUDENT VALUES('Aarav', 'Data Science', 'A', 90)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Meera', 'Data Science', 'B', 100)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Rohan', 'Data Science', 'A', 86)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Ananya', 'DEVOPS', 'A', 50)''')
cursor.execute('''INSERT INTO STUDENT VALUES('Kabir', 'DEVOPS', 'A', 35)''')

## Display all the records
print("The inserted records are")

data=cursor.execute('''Select * From STUDENT''')


for row in data:
    print(row)


    ## Close the Connection

connection.commit()
connection.close()