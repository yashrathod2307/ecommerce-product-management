import sqlite3

conn = sqlite3.connect("products.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

conn.commit()
conn.close()

print("Database created successfully!")