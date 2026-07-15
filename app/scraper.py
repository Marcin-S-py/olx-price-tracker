import requests
from bs4 import BeautifulSoup
import re

def scrape_olx_item(url: str):
    headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error while trying to download site! Status: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

    title_element = soup.find(attrs={"data-cy": "offer_title"})
    title = title_element.get_text(strip=True) if title_element else "Unknown Title"

    price_container = soup.find(attrs={"data-testid": "ad-price-container"})
    
    price_val = None
    if price_container:
        price_element = price_container.find("h3")
        if price_element:
            raw_price = price_element.get_text(strip=True)
            clean_price_str = re.sub(r"[^\d]", "", raw_price)
            if clean_price_str:
                price_val = int(clean_price_str)

    print(f"Scraped Data:\n- Title: {title}\n- Price: {price_val} PLN")

    return {
        "title": title,
        "price": price_val
    }

if __name__ == "__main__":
    test_url = "https://www.olx.pl/d/oferta/jaguar-xf-sportbreak-241-km-4x4-stan-idealny-faktura-vat-marza-nowy-silnik-z-aso-polski-salon-okazja-CID5-ID1bldJO.html?search_reason=search%7Cpromoted"
    scrape_olx_item(test_url)