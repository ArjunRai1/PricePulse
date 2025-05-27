import asyncio
from flask import Flask, jsonify, request
import datetime
import sqlite3
from scraper import fetch_product_data
from apscheduler.schedulers.background import BackgroundScheduler
from db import init_db, save_price, DB_PATH




HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/112.0.0.0 Safari/537.36"
    )
}


    


# def check_price_alerts():
#     alerts = get_active_alerts()
#     for url, email, target_price, current_price, name in alerts:
#         if current_price <= target_price:
#             if send_price_alert(email, name, current_price, target_price, url):
#                 mark_alert_triggered(url, email)

def scrape_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for (url,) in c.execute("SELECT url FROM tracked_urls"):
        try:
            data = asyncio.run(fetch_product_data(url))
            ts = data["timestamp"]
            dt = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            save_price(url, data["name"], data["price"], dt)
            print(f"[OK] {url} Price: ₹{data['price']} at {dt}")
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
    try:
        payload = asyncio.run(fetch_product_data(url.strip()))
        ts = payload["timestamp"]
        dt = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        save_price(url.strip(), payload["name"], payload["price"], dt)
    except Exception as e:
        print("Initial scrape failed:", e)
    return jsonify({"message": "Tracking added", "url": url}), 201

# @app.route("/api/alerts", methods=["POST"])
# def add_alert():
#     data = request.get_json()
#     url = data.get("url")
#     email = data.get("email")
#     target_price = data.get("target_price")
    
#     if not all([url, email, target_price]):
#         return jsonify({"error": "Missing required fields"}), 400
        
#     try:
#         target_price = float(target_price)
#     except ValueError:
#         return jsonify({"error": "Invalid target price"}), 400
        
#     dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     save_alert(url.strip(), email.strip(), target_price, dt)
    
#     # Check if price is already below target
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     latest = c.execute(
#         "SELECT price, name FROM product_price WHERE url=? ORDER BY timestamp DESC LIMIT 1",
#         (url.strip(),)
#     ).fetchone()
#     conn.close()
    
#     if latest and latest[0] <= target_price:
#         if send_price_alert(email.strip(), latest[1], latest[0], target_price, url.strip()):
#             mark_alert_triggered(url.strip(), email.strip())
    
#     return jsonify({"message": "Alert added successfully"}), 201

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
    scheduler.add_job(scrape_all, 'interval', minutes=30, next_run_time=datetime.datetime.now())
    scheduler.start()
    app.run(debug=True)
