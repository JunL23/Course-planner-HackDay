import sqlite3
import csv

def get_db_connection():
    connection = sqlite3.connect("coureses.db")
    return connection

def init():
    conn = get_db_connection()
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS courses (
            course_code TEXT PRIMARY KEY,
            credits INTEGER,
            prerequisites TEXT,
            gen_ed TEXT
        )
        '''
    )
    conn.commit()
    conn.close()

def save_summary(filename, summary):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO pdf_summaries (filename, summary) VALUES (?, ?)',
        (filename, summary)
    )
    conn.commit()
    conn.close()

def csv_to_db(csv_file):
    conn = get_db_connection()

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            conn.execute(
                '''
                INSERT OR IGNORE INTO courses (course_code, credits, prerequisites, gen_ed)
                VALUES (?, ?, ?, ?)
                ''',
                (row[0], row[1], row[2], row[3])
            )
    conn.commit()
    conn.close()

def get_class(class_name):
    conn = get_db_connection()

    cursor = conn.execute(
        'SELECT course_code, credits, prerequisites, gen_ed FROM courses WHERE course_code = ?',
        (class_name,)
    )

    conn.close()

    return cursor.fetchall()