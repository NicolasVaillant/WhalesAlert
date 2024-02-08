import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup

class Scraper:
    async def scrape_trend(self):
        try:
            url = 'https://coinmarketcap.com/trending-cryptocurrencies/'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    content = await response.text()

            soup = BeautifulSoup(content, 'html.parser')

            elements = soup.select('.sc-b8460745-2.cOjIsr')
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
            print('An error occurred while scraping:', e)
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

            return {
                'urlPart': url_part,
                'title': title,
                'changeValue': change_value,
                'changeDirection': change_direction
            }

        except Exception as e:
            print(f'An error occurred while scraping {url_part}:', e)
            return None

# Usage Example
# Note: To run this code, you need to have an event loop
async def main():
    scraper = Scraper()
    results = await scraper.scrape_trend()

    with open(f"./resources/data/trends.json", "r") as f:
        globals_data = json.load(f)
    f.close()

    globals_data = results

    with open(f"./resources/data/trends.json", "w") as f:
        json.dump(globals_data, f, indent=4)

