import asyncio
import time
import datetime
from playwright.async_api import async_playwright
from db import init_db, save_price

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/112.0.0.0 Safari/537.36"
    )
}

async def fetch_product_data(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(extra_http_headers=HEADERS)
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")

        try:
            await page.wait_for_selector("#productTitle", timeout=10000)
        except:
            content = await page.content()
            raise ValueError("Timed out waiting for productTitle;\n" + content[:500])
        
        name = (await page.locator("span#productTitle").inner_text())     
        name = name.strip()
        price_elem = page.locator(".a-price-whole")
        raw = await price_elem.first.inner_text()
        price = float(raw.replace("₹", "").replace(",", "").strip())

        await browser.close()
        return {
            "name": name,
            "price": price,
            "timestamp": int(time.time())
        }

async def main():
    url = ""
    url = url.strip()
    try:
        data = await fetch_product_data(url)
        ts = data['timestamp']
        dt = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        save_price(url, data['name'], data['price'], dt)
        print(f"Saved Name: {data['name']}, Price: ₹{data['price']} at time step: {dt} in database")

    except Exception as e:
        print("[ERROR]", e)

if __name__ == "__main__":
    init_db()
    asyncio.run(main())
