import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup
from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler
from os import name, system
import aiofiles

if name == "nt":
    # Version PC
    losers_json = Path("resources", "data_scrap", "losers.json")
    logo_dir = Path("resources", "logos")
else:
    # Version serveur
    losers_json = Path("/home", "container", "webroot", "resources", "data_scrap", "losers.json")
    logo_dir = Path("/home", "container", "webroot", "resources", "logos")

# Create logo directory if not exists
logo_dir.mkdir(parents=True, exist_ok=True)

#----------------------------------------------------
# Logging
#----------------------------------------------------
logger_fonction_scrap = logging.getLogger('scraping')
if not logger_fonction_scrap.handlers:
    logger_fonction_scrap.setLevel(logging.INFO)
    filenamelog = Path("logs", f"scrap").with_suffix(".log")
    handler = TimedRotatingFileHandler(filenamelog, when='midnight', interval=1, backupCount=7, encoding='utf-8')
    handler.suffix = "%Y-%m-%d"  # suffixe le fichier de log avec la date du jour
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger_fonction_scrap.addHandler(handler)

class ScraperL:
    async def download_logo(self, session, url, name):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    name_c = str(name).lower()
                    file_path = logo_dir / f"{name_c}.png"
                    async with aiofiles.open(file_path, 'wb') as f:
                        content = await response.read()
                        await f.write(content)
        except Exception as e:
            logger_fonction_scrap.error(f"An error occurred while downloading logo for {name}: {e}")

    async def scrape_losers(self):
        try:
            url = 'https://coinmarketcap.com/gainers-losers/'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    content = await response.text()

                soup = BeautifulSoup(content, 'html.parser')

                # Select the "Top Losers" table
                header_element = next((h for h in soup.find_all('h3') if "Top Losers" in h.text), None)
                table_wrap = header_element.find_previous('div', class_='uikit-col-md-8').select_one('.table-wrap tbody') if header_element else None

                if not table_wrap:
                    logger_fonction_scrap.error("Could not find the Top Losers table.")
                    return []

                rows = table_wrap.select('tr')
                extracted_data = []

                for row in rows[:3]:
                    # Extract the cryptocurrency name
                    name_element = row.select_one('td:nth-child(2) p[font-weight="semibold"]')
                    name = name_element.text.strip() if name_element else None

                    # Extract the cryptocurrency symbol
                    symbol_element = row.select_one('td:nth-child(2) p[class*="coin-item-symbol"]')
                    symbol = symbol_element.text.strip() if symbol_element else None

                    # Extract the price change percentage
                    price_change_element = row.select_one('td:nth-child(4) span[class*="sc-a59753b0-0"]')
                    price_change = price_change_element.text.strip() if price_change_element else None

                    # Extract the market cap
                    market_cap_element = row.select_one('td:nth-last-child(1)')
                    market_cap = market_cap_element.text.strip() if market_cap_element else None

                    # Extract href to detail page
                    link_element = row.select_one('td:nth-child(2) a')
                    href = link_element['href'] if link_element else None
                    specific_part_of_href = href.split('/')[2] if href else None

                    # Extract logo URL
                    logo_element = row.select_one('td:nth-child(2) img.coin-logo')
                    logo_url = logo_element['src'] if logo_element else None

                    if logo_url and name:
                        await self.download_logo(session, logo_url, name)

                    extracted_data.append({
                        'urlPart': name,
                        'title': symbol,
                        'changeValue': price_change,
                        'changeDirection': "down"
                    })

            return extracted_data

        except Exception as e:
            logger_fonction_scrap.error("An error occurred while scraping the Losers section:", e)
            return []

async def main():
    scraper = ScraperL()
    results = await scraper.scrape_losers()

    with open(losers_json, "r") as f:
        globals_data = json.load(f)
    f.close()

    globals_data = results

    with open(losers_json, "w") as f:
        json.dump(globals_data, f, indent=4)
