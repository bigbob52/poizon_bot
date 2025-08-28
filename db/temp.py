import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "bot.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# cur.execute("DELETE FROM users WHERE user_id = ?", ('7397907288',))
cur.execute("UPDATE users SET username = NULL WHERE username = 'no username'")
conn.commit()