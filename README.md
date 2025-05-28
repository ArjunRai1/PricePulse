## Current Tech Stack
- **Backend**: Flask  
- **Database**: SQLite  
- **Scheduler**: APScheduler  
- **Frontend**: React + Chart.js  
- **Deployment**: Render

# PricePulse

PricePulse empowers users to:

- **Instantly snapshot** the current price, product name, and metadata of any e-commerce listing by submitting its URL.  
- **Continuously monitor** that product every 30 minutes, building a complete price history.  
- **Visualize trends** in a sleek React interface, helping users identify ideal purchase windows.  
- **Threshold alerts** via email so you never miss a deal when the price dips below your target.  

Under the hood, PricePulse leverages a lightweight Flask API, Playwright-driven scraping, a SQLite database for persistence, and a React single-page app for the user interface. This combination delivers a fast initial response and hands-off ongoing monitoring without requiring users to run any local software.

---

## 📁 Repository Structure
- /
- ├── backend/
- │ ├── app.py # Flask application: API endpoints, CORS, DB init & scheduler
- │ ├── db.py # SQLite helpers: init_db(), save_price(), fetch_history()
- │ ├── scraper.py # Async Playwright scraper + scrape_all() loop for batch jobs
- │ ├── requirements.txt # Python dependencies (Flask, flask-cors, playwright, etc.)
- │ └── prices.db # SQLite database (auto-created on first run)
- │
- ├── frontend/
- │ ├── public/ # Static assets (index.html, icons, etc.)
- │ ├── src/
- │ │ ├── config.js # Reads REACT_APP_API_URL from environment
- │ │ ├── App.js # Core UI component, form & table rendering
- │ │ ├── services/ # API wrappers for /api/track and /api/history
- │ │ └── components/ # Reusable UI pieces (Table, Form, Loader)
- │ ├── package.json # Build & start scripts, proxy for local dev
- │ └── .env.example # Template for REACT_APP_API_URL
- │
- ├── .gitignore
- └── README.md

## 📋 Detailed Description

PricePulse was born from the common frustration of manually checking product pages for price drops. Rather than relying on browser plugins or bookmarking, PricePulse offers:

1. **Immediate Insight**  
   - Submit any product URL (Amazon, Flipkart, eBay, etc.) and receive back the exact price, product title, and timestamp within seconds.  
   - No page-by-page copying—our scraper handles the heavy lifting.

2. **Hands-Off Monitoring**  
   - Once tracked, PricePulse will automatically re-scrape the product every 30 minutes.  
   - All data is stored chronologically, letting you chart price fluctuations over hours, days, or weeks.

3. **User-Centered UI**  
   - A clean React SPA displays the current snapshot and full history in a sortable, paginated table.  
   - Future enhancements include graph visualizations and custom alert thresholds.

4. **Lightweight & Extensible**  
   - The backend uses SQLite for zero-config persistence; you can swap it out for Postgres if you scale up.  
   - Playwright ensures robust scraping across modern dynamic sites.  
   - React and Flask form a familiar stack—developers can easily customize or extend functionality.

5. **Future Roadmap**  
   - **Threshold Alerts:** Email or SMS notifications when the price crosses your target.  
   - **Multi-Site Support:** Automatic detection for popular e-commerce platforms.  
   - **User Accounts:** Personalized watchlists and historical analytics dashboards.  

---

## 🚀 Local Setup

### Prerequisites

- **Node.js** (v16+) & **npm**  
- **Python** (3.9+) & **pip**  
- **Playwright** (for browser automation)  
 

### 1. Clone the Repository

### 2. Backend
git clone https://github.com/ArjunRai1/PricePulse
pip install -r requirements.txt
playwright install
Run pythen backend/app.py

### 3. Frontend
cd frontend
npm start