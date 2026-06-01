import sqlite3
import pandas as pd
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "..", "lunaflow.db")

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_wellness_db():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='wellness_logs'")
    if c.fetchone() is None:
        c.execute('''
            CREATE TABLE wellness_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                mood TEXT,
                energy INTEGER,
                stress INTEGER,
                sleep REAL,
                water INTEGER,
                notes TEXT,
                UNIQUE(user_id, date)
            )
        ''')
    else:
        try:
            c.execute("SELECT user_id FROM wellness_logs LIMIT 1")
        except sqlite3.OperationalError:
            c.execute("ALTER TABLE wellness_logs RENAME TO wellness_logs_old")
            c.execute('''
                CREATE TABLE wellness_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    mood TEXT,
                    energy INTEGER,
                    stress INTEGER,
                    sleep REAL,
                    water INTEGER,
                    notes TEXT,
                    UNIQUE(user_id, date)
                )
            ''')
            c.execute("INSERT INTO wellness_logs (user_id, date, mood, energy, stress, sleep, water, notes) SELECT 1, date, mood, energy, stress, sleep, water, notes FROM wellness_logs_old")
            c.execute("DROP TABLE wellness_logs_old")

    conn.commit()
    conn.close()

def save_wellness_log(user_id, date_val, mood, energy, stress, sleep, water, notes):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO wellness_logs (user_id, date, mood, energy, stress, sleep, water, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, date) DO UPDATE SET
            mood=excluded.mood,
            energy=excluded.energy,
            stress=excluded.stress,
            sleep=excluded.sleep,
            water=excluded.water,
            notes=excluded.notes
    ''', (user_id, date_val.strftime("%Y-%m-%d"), mood, energy, stress, sleep, water, notes))
    conn.commit()
    conn.close()

def get_all_wellness_logs(user_id):
    conn = get_connection()
    df = pd.read_sql_query(f'SELECT * FROM wellness_logs WHERE user_id = {user_id} ORDER BY date', conn)
    conn.close()
    if not df.empty:
        df['date'] = pd.to_datetime(df['date']).dt.date
    return df

def get_latest_wellness_log(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT date, mood, energy, stress, sleep, water, notes FROM wellness_logs WHERE user_id = ? ORDER BY date DESC LIMIT 1', (user_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {
            'date': row[0],
            'mood': row[1],
            'energy': row[2],
            'stress': row[3],
            'sleep': row[4],
            'water': row[5],
            'notes': row[6]
        }
    return None
