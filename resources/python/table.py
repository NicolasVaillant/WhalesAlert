import requests
import json
from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler
from os import name, system

if name == "nt":
    # Version pc
    table_jaon = Path("resources", "data_scrap", "main.json")
else :
    # Version serveur
    table_jaon = Path("/home", "container", "webroot","resources", "data_scrap", "main.json")

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

class CoinFetcher:
    def __init__(self):
        self.api_key = '4b3b4ea4-0770-4d97-8db7-a62f4f5148c9'
        self.coins = self.fetch_data()

    def fetch_data(self):
        headers = {
            'X-CMC_PRO_API_KEY': self.api_key,
        }
        params = {
            'start': 1,
            'limit': 5000,  # Exemple de limite
        }
        response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest', headers=headers, params=params)
        data = response.json()
        formatted_data = self.format_data(data['data'])
        return formatted_data

    def format_data(self, data):
        formatted_coins = []
        for coin in data:
            coin_name = coin['name']
            if coin_name == "BNB":
                coin['name'] = "Binance Coin"
            elif coin_name == "Tether USDt" or coin_name == "Tether_USDt":
                coin['name'] = "Tether"
            
            price = float(coin['quote']['USD']['price'])
            # Format fixe pour tous les prix avec 8 décimales
            price = f"{price:.8f}"
            if float(price) >= 0.1:
                coin['quote']['USD']['price'] = str(round(float(price),2))
            else :
                coin['quote']['USD']['price'] = price.rstrip('0').rstrip('.') if '.' in price else price
            
            formatted_coin = {
                "Rank": coin['cmc_rank'],
                "Name": coin['name'],
                "Symbol": coin['symbol'],
                "Price": f"{coin['quote']['USD']['price']}",
                "Volume": f"{coin['quote']['USD']['volume_24h']:.2f}",
                "1h": f"{coin['quote']['USD']['percent_change_1h']:.2f}%",
                "24h": f"{coin['quote']['USD']['percent_change_24h']:.2f}%",
                "7d": f"{coin['quote']['USD']['percent_change_7d']:.2f}%",
            }
            formatted_coins.append(formatted_coin)
        return {"cryptocurrencies": formatted_coins}

# Lecture des données existantes et mise à jour avec les nouvelles données
def update_global_data(new_data):
    try:
        with open(table_jaon, "r") as f:
            globals_data = json.load(f)
    except FileNotFoundError:
        globals_data = {}
    # Mise à jour ou ajout de nouvelles données
    globals_data.update(new_data)

    # Sauvegarde des données mises à jour dans le fichier
    with open(table_jaon, "w") as f:
        json.dump(globals_data, f, indent=4)
