import requests
import os
import json
from pathlib import Path

# Version pc
chemin_base = Path("resources", "data_coins")

# Version serveur
# chemin_base = Path("/home", "container", "webroot","resources", "data_coins")

# S'assurer que le chemin de base existe
if not os.path.exists(chemin_base):
    os.makedirs(chemin_base)

def fetch_coin_details(symbol, name):
    """
    Fonction pour récupérer les détails d'une cryptomonnaie depuis CoinCodex et les enregistrer dans un fichier JSON dans le chemin spécifié.
    """
    url = f"https://coincodex.com/api/coincodex/get_coin/{symbol}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            coin_details = response.json()
            # Créer un nom de fichier valide et spécifique pour chaque cryptomonnaie
            filename = f"{name.replace('/', '_').replace(' ', '_').lower()}.json"
            chemin_fichier = os.path.join(chemin_base, filename)
            with open(chemin_fichier, 'w') as file:
                json.dump(coin_details, file, indent=4)
            print(f"Details for {symbol} saved to {filename}.")
        else:
            print(f"Failed to fetch data for {symbol}. Status code:", response.status_code)
    except Exception as e:
        print(f"An error occurred while fetching data for {symbol}:", e)

def fetch_coins_and_process():
    """
    Fonction pour récupérer les données des cryptomonnaies depuis l'API CoinPaprika, les sauvegarder, puis récupérer des détails supplémentaires pour chaque cryptomonnaie depuis CoinCodex.
    """
    url = "https://api.coinpaprika.com/v1/coins"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            coins = response.json()
            for coin in coins[:5000]:  # Limiter pour cet exemple
                fetch_coin_details(coin['symbol'], coin['name'])
        else:
            print("Failed to fetch data from CoinPaprika API. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)
