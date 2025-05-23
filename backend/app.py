import asyncio
from flask import Flask, jsonify, request
import time, datetime
import sqlite3
from scraper import fetch_product_data
from apscheduler.schedulers.background import BackgroundScheduler
from playwright.async_api import async_playwright
from db import init_db, save_price, DB_PATH

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/112.0.0.0 Safari/537.36"
    )
}

def scrape_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for (url,) in c.execute("SELECT url FROM tracked_urls"):
        try:
            data = asyncio.run(fetch_product_data(url))
            ts = data["timestamp"]
            dt = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            save_price(url, data["name"], data["price"], dt)
            print(f"[OK] {url} → ₹{data['price']} @ {dt}")
        except Exception as e:
            print(f"[ERR] {url}: {e}")
    conn.close()

app = Flask(__name__)

@app.route("/api/track", methods=["POST"])
def add_url():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing url"}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO tracked_urls (url) VALUES (?)", (url.strip(),))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()
    return jsonify({"message": "Tracking added", "url": url}), 201

@app.route("/api/history", methods=["GET"])
def get_history():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing url param"}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute(
        "SELECT name, price, timestamp FROM product_price WHERE url=? ORDER BY id",
        (url.strip(),)
    ).fetchall()
    conn.close()

    history = [
        {"name": name, "price": price, "timestamp": ts}
        for name, price, ts in rows
    ]
    return jsonify({"url": url, "history": history})

if __name__ == "__main__":
    init_db()

    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_all, 'cron', minute=0)
    scheduler.start()
    app.run(debug=True)
