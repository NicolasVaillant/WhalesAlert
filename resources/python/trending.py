import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup
from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler

from os import name, system

if name == "nt":
    # Version pc
    trends_jaon = Path("resources", "data_scrap", "trends.json")
else :
    # Version serveur
    trends_jaon = Path("/home", "container", "webroot","resources", "data_scrap", "trends.json")

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

class Scraper:
    async def scrape_trend(self):
        try:
            url = 'https://coinmarketcap.com/trending-cryptocurrencies/'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    content = await response.text()

            soup = BeautifulSoup(content, 'html.parser')

            elements = soup.select('.sc-44b98da2-2.kjRmyt')
            extracted_data = []

            for element in elements[:3]:
                parent_row = element.find_parent('tr')
                if parent_row:
                    link_element = parent_row.select_one('a.cmc-link')
                    if link_element:
                        href = link_element['href']
                        specific_part_of_href = href.split('/')[2]
                        extracted_data.append({
                            'href': href,
                            'text': link_element.text.strip(),
                            'specific_part_of_href': specific_part_of_href
                        })

            details = await asyncio.gather(*[self.scrape_specific_info(entry['specific_part_of_href']) for entry in extracted_data])

            return details

        except Exception as e:
            logger_fonction_scrap.error('An error occurred while scraping:', e)
            return []

    async def scrape_specific_info(self, url_part):
        try:
            url = f'https://coinmarketcap.com/currencies/{url_part}/'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    content = await response.text()

            soup = BeautifulSoup(content, 'html.parser')
            title = soup.title.string.split(',')[1].replace("to USD live price", "").strip() if soup.title else None

            change_element = soup.select_one('[data-change="up"], [data-change="down"]')
            change_value = None
            change_direction = None

            if change_element:
                change_value = change_element.text.strip().replace("(1d)", "").replace(".", ",")
                change_value = change_value.replace('\xa0', '')  # Remove '\xa0'
                change_direction = change_element.attrs['data-change']
            url_part = url_part.replace("-","_")
            return {
                'urlPart': url_part,
                'title': title,
                'changeValue': change_value,
                'changeDirection': change_direction
            }

        except Exception as e:
            logger_fonction_scrap.error(f'An error occurred while scraping {url_part}:', e)
            return None

async def main():
    scraper = Scraper()
    results = await scraper.scrape_trend()

    with open(trends_jaon, "r") as f:
        globals_data = json.load(f)
    f.close()

    globals_data = results

    with open(trends_jaon, "w") as f:
        json.dump(globals_data, f, indent=4)

