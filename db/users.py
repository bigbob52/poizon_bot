import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "bot.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    orders INTEGER DEFAULT 0,
    bonus INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# --- FUNCTIONS ---
def add_user(user_id: int, username: str):
    # cur.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    # if cur.fetchone() is None:
    #     cur.execute(
    #         "INSERT INTO users (user_id, username, orders, bonus) VALUES (?, ?, 0, 0)",
    #         (user_id, username)
    #     )
    #     conn.commit()

    cur.execute(
        "INSERT OR IGNORE INTO users (user_id, username, orders, bonus) VALUES (?, ?, 0, 0)",
        (user_id, username)
    )
    conn.commit()

def get_user_by_id(user_id: int):
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    return dict(row) if row else None

def get_user_by_username(username: str):
    cur.execute("SELECT * FROM users WHERE username = ?", (username, ))
    row = cur.fetchone()
    return dict(row) if row else None

def update_orders(user_id: int, amount: int):
    cur.execute("UPDATE users SET orders = ? WHERE user_id = ?", (amount, user_id,))
    conn.commit()

def update_bonus(user_id: int, amount: int):
    cur.execute("UPDATE users SET bonus = bonus + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()

def get_user_by_order_id(order_id: int):
    cur.execute("""
        SELECT u.* FROM users u
        JOIN orders o ON u.user_id = o.user_id
        WHERE o.order_id = ?
    """, (order_id,))
    row = cur.fetchone()
    return dict(row) if row else None

def get_all_users():
    cur.execute("SELECT * FROM users ORDER BY created_at DESC")
    return [dict(row) for row in cur.fetchall()]