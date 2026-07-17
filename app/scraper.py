import httpx
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

async def scrape_olx_offer(url: str) -> dict | None:
    async with httpx.AsyncClient(headers=HEADERS, timeout=10.0) as client:
        try:
            response = await client.get(url, follow_redirects=True)
            if response.status_code != 200:
                return None
        except httpx.RequestError:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.find(attrs={"data-cy": "offer_title"})
        title = title_tag.get_text(strip=True) if title_tag else None

        price_tag = soup.find(attrs={"data-testid": "ad-price-container"})
        price = None

        if price_tag:
            price_text = price_tag.get_text(strip=True)
            if "darmo" in price_text.lower() or "zamien" in price_text.lower():
                price = 0.0
            else:
                cleaned_price = re.sub(r"[^\d.,]", "", price_text).replace(",", ".")
                try:
                    price = float(cleaned_price)
                except ValueError:
                    price = None
        return {"title": title, "price": price}