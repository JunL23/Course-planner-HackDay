from database import init, csv_to_db, get_db_connection

init()

csv_to_db("all_courses.csv")

# Check and print all rows in the courses table
conn = get_db_connection()
cursor = conn.execute('SELECT * FROM courses')
for row in cursor.fetchall():
    print(row)

cursor = conn.execute('select count(distinct(course_code)) from courses')
print(cursor.fetchone()[0])


conn.close()