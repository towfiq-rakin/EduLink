import sqlite3
import os
import hashlib

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "accounts.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_table_and_seed():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            usertype TEXT NOT NULL CHECK(usertype IN ('student', 'teacher', 'administrator'))
        )""")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        # Add sample teacher users
        users = [
            ("teacher1", hash_password("password1"), "teacher"),
            ("teacher2", hash_password("password2"), "teacher"),
        ]
        cur.executemany("INSERT INTO users (username, password, usertype) VALUES (?, ?, ?)", users)
        conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password, usertype FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return row[1]  # Return usertype
    return None

