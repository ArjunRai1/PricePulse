import sqlite3

DB_PATH = "prices.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    #c.execute("PRAGMA journal_mode = WAL;")
    c.execute("""
    CREATE TABLE IF NOT EXISTS product_price(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        timestamp TEXT NOT NULL
    );""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS tracked_urls(
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        url  TEXT NOT NULL UNIQUE
    );""")
   
    conn.commit()
    conn.close()

def save_price(url: str, name: str, price: float, timestamp: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""INSERT INTO product_price (url, name, price, timestamp) VALUES (?, ?, ?, ?)""", (url, name, price, timestamp))
    conn.commit()
    conn.close()
