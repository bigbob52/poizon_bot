import sqlite3
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data/bot.db")

# Создаём резервную копию базы на всякий случай
shutil.copy(DB_PATH, DB_PATH + ".backup")

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

# 1. Создаем новую таблицу с ON DELETE CASCADE
cur.execute("""
CREATE TABLE IF NOT EXISTS order_items_new (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    link TEXT,
    size TEXT,
    price INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
)
""")

# 2. Переносим данные из старой таблицы
cur.execute("""
INSERT INTO order_items_new (item_id, order_id, link, size, price)
SELECT item_id, order_id, link, size, price FROM order_items
""")

# # 3. Удаляем старую таблицу
cur.execute("DROP TABLE order_items")
# cur.execute("ALTER TABLE order_items RENAME TO order_items_old")

# 4. Переименовываем новую таблицу
cur.execute("ALTER TABLE order_items_new RENAME TO order_items")

conn.commit()
conn.close()

print("Миграция завершена! Резервная копия базы сохранена как bot.db.backup")