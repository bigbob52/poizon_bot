import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "bot.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()


# Таблица заказов
cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    status TEXT DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

# Таблица товаров в заказе
cur.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    link TEXT,
    size TEXT,
    price INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
)
""")

# ⚡ Сместить автоинкремент если таблица orders пуста
cur.execute("SELECT COUNT(*) FROM orders")
if cur.fetchone()[0] == 0:
    cur.execute("DELETE FROM sqlite_sequence WHERE name = 'orders'")
    cur.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('orders', 325)")

conn.commit()


# --- FUNCTIONS ---
def create_order(user_id: int, items: list[dict]) -> int:
    """Создает новый заказ и добавляет товары"""
    cur.execute("INSERT INTO orders (user_id) VALUES (?)", (user_id,))
    order_id = cur.lastrowid

    for item in items:
        cur.execute(
            "INSERT INTO order_items (order_id, link, size, price) VALUES (?, ?, ?, ?)",
            (order_id, item["link"], item["size"], item["price"])
        )

    conn.commit()
    return order_id

def get_order(order_id: int) -> tuple[dict | None, list[dict]]:
    """Получить заказ с товарами"""
    cur.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cur.fetchone()

    # нет заказа с таким айди
    if not order:
        return None, []

    cur.execute("SELECT link, size, price FROM order_items WHERE order_id = ?", (order_id,))
    items = [dict(row) for row in cur.fetchall()]

    return dict(order), items

def get_user_orders(user_id: int):
    cur.execute("SELECT * FROM orders WHERE user_id = ? AND status != 'deleted' ORDER BY created_at DESC", (user_id,))
    return [dict(row) for row in cur.fetchall()]

def update_order_status(order_id: int, status: str):
    """Обновить статус заказа"""
    cur.execute("UPDATE orders SET status = ? WHERE order_id = ?", (status, order_id))
    conn.commit()

def delete_order(order_id: int):
    """Удалить заказ (товары удаляются автоматически через ON DELETE CASCADE)"""
    # cur.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
    # cur.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
    cur.execute("UPDATE orders SET status = 'deleted' WHERE order_id = ?", (order_id,))
    conn.commit()

def get_all_actual_orders() -> list[dict]:
    """Получить все заказы со статусами new, accepted"""
    cur.execute("SELECT * FROM orders WHERE status != 'deleted' ORDER BY created_at")
    return [dict(row) for row in cur.fetchall()]

def count_all_orders() -> int:
    cur.execute("SELECT COUNT(*) FROM orders")
    return cur.fetchone()[0]

def count_orders_for_period(start_time: datetime) -> int:
    cur.execute("SELECT COUNT(*) FROM orders WHERE created_at >= ?",
                (start_time.strftime("%Y-%m-%d %H:%M:%S"),),
    )
    return cur.fetchone()[0]