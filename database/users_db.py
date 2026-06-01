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
            age INTEGER DEFAULT 25,
            fcm_token TEXT DEFAULT '',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Safe Migration for missing columns
    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]
    if 'age' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN age INTEGER DEFAULT 25")
    if 'fcm_token' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN fcm_token TEXT DEFAULT ''")
        
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

def get_user_profile(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT name, email, age, fcm_token FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return {"name": user[0], "email": user[1], "age": user[2], "fcm_token": user[3]}
    return None

def update_user_profile(user_id, name, age):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (name, age, user_id))
    conn.commit()
    conn.close()

def save_fcm_token(user_id, token):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET fcm_token = ? WHERE id = ?', (token, user_id))
    conn.commit()
    conn.close()
