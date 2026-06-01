import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "..", "lunaflow.db")
def get_connection():
    return sqlite3.connect(DB_NAME)

def migrate_or_create(c, table_name, create_sql, columns):
    c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if c.fetchone() is None:
        c.execute(create_sql)
    else:
        try:
            c.execute(f"SELECT user_id FROM {table_name} LIMIT 1")
        except sqlite3.OperationalError:
            c.execute(f"ALTER TABLE {table_name} RENAME TO {table_name}_old")
            c.execute(create_sql)
            c.execute(f"INSERT INTO {table_name} (user_id, {columns}) SELECT 1, {columns} FROM {table_name}_old")
            c.execute(f"DROP TABLE {table_name}_old")

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    migrate_or_create(c, 'cycles', '''
        CREATE TABLE cycles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            last_period_start DATE NOT NULL,
            cycle_length INTEGER NOT NULL,
            period_duration INTEGER NOT NULL
        )
    ''', "last_period_start, cycle_length, period_duration")

    migrate_or_create(c, 'symptoms', '''
        CREATE TABLE symptoms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            cramps BOOLEAN,
            mood_swings BOOLEAN,
            headache BOOLEAN,
            acne BOOLEAN,
            fatigue BOOLEAN,
            bloating BOOLEAN,
            UNIQUE(user_id, date)
        )
    ''', "date, cramps, mood_swings, headache, acne, fatigue, bloating")

    migrate_or_create(c, 'chat_history', '''
        CREATE TABLE chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''', "role, content, timestamp")

    migrate_or_create(c, 'water_logs', '''
        CREATE TABLE water_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            glasses INTEGER NOT NULL,
            UNIQUE(user_id, date)
        )
    ''', "date, glasses")

    c.execute('''
        CREATE TABLE IF NOT EXISTS wellness_tips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            tip TEXT NOT NULL,
            UNIQUE(user_id, date)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            type TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS notification_settings (
            user_id INTEGER PRIMARY KEY,
            period_reminder_days TEXT DEFAULT '7,3,1',
            water_reminder_interval TEXT DEFAULT 'Off',
            wellness_reminder BOOLEAN DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

def save_cycle(user_id, last_period_start, cycle_length, period_duration):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO cycles (user_id, last_period_start, cycle_length, period_duration)
        VALUES (?, ?, ?, ?)
    ''', (user_id, last_period_start.strftime("%Y-%m-%d"), cycle_length, period_duration))
    conn.commit()
    conn.close()

def get_latest_cycle(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT last_period_start, cycle_length, period_duration FROM cycles WHERE user_id = ? ORDER BY id DESC LIMIT 1', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'last_period_start': datetime.strptime(row[0], "%Y-%m-%d").date(),
            'cycle_length': row[1],
            'period_duration': row[2]
        }
    return None

def get_all_cycles(user_id):
    conn = get_connection()
    df = pd.read_sql_query(f'SELECT * FROM cycles WHERE user_id = {user_id} ORDER BY last_period_start', conn)
    conn.close()
    if not df.empty:
        df['last_period_start'] = pd.to_datetime(df['last_period_start']).dt.date
    return df

def save_symptoms(user_id, date_val, cramps, mood_swings, headache, acne, fatigue, bloating):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO symptoms (user_id, date, cramps, mood_swings, headache, acne, fatigue, bloating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, date) DO UPDATE SET
            cramps=excluded.cramps,
            mood_swings=excluded.mood_swings,
            headache=excluded.headache,
            acne=excluded.acne,
            fatigue=excluded.fatigue,
            bloating=excluded.bloating
    ''', (user_id, date_val.strftime("%Y-%m-%d"), cramps, mood_swings, headache, acne, fatigue, bloating))
    conn.commit()
    conn.close()

def get_all_symptoms(user_id):
    conn = get_connection()
    df = pd.read_sql_query(f'SELECT * FROM symptoms WHERE user_id = {user_id} ORDER BY date', conn)
    conn.close()
    if not df.empty:
        df['date'] = pd.to_datetime(df['date']).dt.date
    return df

def save_chat_message(user_id, role, content):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO chat_history (user_id, role, content)
        VALUES (?, ?, ?)
    ''', (user_id, role, content))
    conn.commit()
    conn.close()

def get_chat_history(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT role, content FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC', (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]

def clear_chat_history(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM chat_history WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def save_water_log(user_id, date_val, glasses):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO water_logs (user_id, date, glasses)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, date) DO UPDATE SET glasses=excluded.glasses
    ''', (user_id, date_val.strftime("%Y-%m-%d"), glasses))
    conn.commit()
    conn.close()

def get_water_log(user_id, date_val):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT glasses FROM water_logs WHERE user_id = ? AND date = ?', (user_id, date_val.strftime("%Y-%m-%d")))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def get_notification_settings(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT period_reminder_days, water_reminder_interval, wellness_reminder FROM notification_settings WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            'period_reminder_days': row[0].split(',') if row[0] else [],
            'water_reminder_interval': row[1],
            'wellness_reminder': bool(row[2])
        }
    return {
        'period_reminder_days': ['7', '3', '1'],
        'water_reminder_interval': 'Off',
        'wellness_reminder': True
    }

def save_notification_settings(user_id, period_days, water_interval, wellness_reminder):
    conn = get_connection()
    c = conn.cursor()
    period_str = ",".join(period_days)
    c.execute('''
        INSERT INTO notification_settings (user_id, period_reminder_days, water_reminder_interval, wellness_reminder)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            period_reminder_days=excluded.period_reminder_days,
            water_reminder_interval=excluded.water_reminder_interval,
            wellness_reminder=excluded.wellness_reminder
    ''', (user_id, period_str, water_interval, int(wellness_reminder)))
    conn.commit()
    conn.close()
