import requests
import json

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
            formatted_coin = {
                "Rank": coin['cmc_rank'],
                "Name": coin['name'],
                "Symbol": coin['symbol'],
                "Price": f"{coin['quote']['USD']['price']:.2f}",
                "Volume": f"{coin['quote']['USD']['volume_24h']:.2f}",
                "1h": f"{coin['quote']['USD']['percent_change_1h']:.2f}%",
                "24h": f"{coin['quote']['USD']['percent_change_24h']:.2f}%",
                "7d": f"{coin['quote']['USD']['percent_change_7d']:.2f}%",
            }
            formatted_coins.append(formatted_coin)
        return {"cryptocurrencies": formatted_coins}

# Lecture des données existantes et mise à jour avec les nouvelles données
def update_global_data(new_data):
    file_path = "./resources/data_scrap/main.json"
    try:
        with open(file_path, "r") as f:
            globals_data = json.load(f)
    except FileNotFoundError:
        globals_data = {}

    # Mise à jour ou ajout de nouvelles données
    globals_data.update(new_data)

    # Sauvegarde des données mises à jour dans le fichier
    with open(file_path, "w") as f:
        json.dump(globals_data, f, indent=4)


