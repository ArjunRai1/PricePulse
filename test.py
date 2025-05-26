import asyncio
import time
from playwright.async_api import async_playwright

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
    url = "https://www.amazon.in/HP-Powered-16-1-inch-Backlit-s0089AX/dp/B0CNR7KRSC/?_encoding=UTF8&pd_rd_w=aCxHU&content-id=amzn1.sym.0e03aefb-8b93-49f8-beeb-6d21836a1b3d&pf_rd_p=0e03aefb-8b93-49f8-beeb-6d21836a1b3d&pf_rd_r=3FE3VFD5AWDVADBYG511&pd_rd_wg=5W8Zv&pd_rd_r=6489b737-7aea-4104-b524-3366513f2469&ref_=pd_hp_d_atf_dealz_cs&th=1"
    url = url.strip()
    try:
        data = await fetch_product_data(url)
        print(f"Name: {data['name']}, Price: ₹{data['price']} at time step: {data['timestamp']}")
    except Exception as e:
        print("[ERROR]", e)

if __name__ == "__main__":
    asyncio.run(main())

