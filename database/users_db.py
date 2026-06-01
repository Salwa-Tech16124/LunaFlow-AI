import sqlite3
import hashlib
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "..", "lunaflow.db")

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_users_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(name, email, password):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
        ''', (name, email.lower(), hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT id, name FROM users WHERE email = ? AND password_hash = ?
    ''', (email.lower(), hash_password(password)))
    user = c.fetchone()
    conn.close()
    if user:
        return {"id": user[0], "name": user[1]}
    return None
