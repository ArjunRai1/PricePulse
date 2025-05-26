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


# def send_price_alert(to_email, product_name, current_price, target_price, product_url):
#     """Send an SMTP email alert when price hits the target."""
#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT", 587))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_pass = os.getenv("SMTP_PASS")

#     subject = f"[PricePulse] '{product_name}' is now ₹{current_price}"
#     body = f"""Good news! The price of '{product_name}' has dropped to ₹{current_price}, which meets your target of ₹{target_price}. View it here: {product_url}"""

#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = smtp_user
#     msg["To"] = to_email

#     with smtplib.SMTP(smtp_host, smtp_port) as smtp:
#         smtp.starttls()
#         smtp.login(smtp_user, smtp_pass)
#         smtp.send_message(msg)


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
