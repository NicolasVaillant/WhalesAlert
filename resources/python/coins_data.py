import requests
import os
import json
from pathlib import Path
from os import name, system
import logging
from logging.handlers import TimedRotatingFileHandler

if name == "nt":
    # Version pc
    chemin_base = Path("resources", "data_coins")
    coin_list_file = Path("resources", "data_scrap", "coins_list.json")
else :
    # Version serveur
    chemin_base = Path("/home", "container", "webroot","resources", "data_coins")
    coin_list_file = Path("/home", "container", "webroot","resources", "data_scrap", "coins_list.json")

# S'assurer que le chemin de base existe
if not os.path.exists(chemin_base):
    os.makedirs(chemin_base)

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

def fetch_coin_details(symbol, name, active):
    """
    Fonction pour récupérer les détails d'une cryptomonnaie depuis CoinCodex et les enregistrer dans un fichier JSON dans le chemin spécifié.
    """
    symbol = str(symbol).split('-')[0]
    url = f"https://coincodex.com/api/coincodex/get_coin/{symbol}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            coin_details = response.json()
            if active == True:
                # Créer un nom de fichier valide et spécifique pour chaque cryptomonnaie
                filename = f"{name.replace('/', '_').replace(' ', '_').replace('-','_').lower()}.json"
                chemin_fichier = os.path.join(chemin_base, filename)
                if os.path.exists(chemin_fichier):
                    with open(chemin_fichier, 'r') as file:
                        data_file = json.load(file)
                    symbol_file = data_file['symbol']
                    if str(symbol_file).lower() == symbol :
                        with open(chemin_fichier, 'w') as file:
                            json.dump(coin_details, file, indent=4)
                        file.close()
                        logger_fonction_scrap.info(f"Details for {symbol} saved to {filename}.")
                    else :
                        logger_fonction_scrap.error(f"Failed to fetch file {filename} for {symbol}. Status code:{response.status_code}")
                else:
                    with open(chemin_fichier, 'w') as file:
                        json.dump(coin_details, file, indent=4)
                        logger_fonction_scrap.info(f"Details for {symbol} saved to {filename}.")
                    file.close()
        else:
            logger_fonction_scrap.error(f"Failed to fetch data for {symbol}. Status code:{response.status_code}")
    except Exception as e:
        logger_fonction_scrap.error(f"An error occurred while fetching data for {symbol}: {e}")

def fetch_and_save_coins_data():
    """
    Fonction pour récupérer les données des cryptomonnaies depuis l'API CoinPaprika et les sauvegarder dans un fichier JSON.
    """
    url = "https://api.coinpaprika.com/v1/coins"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            coins = response.json()
            with open(coin_list_file, 'w') as json_file:
                json.dump(coins, json_file, indent=4)
            logger_fonction_scrap.info("Data successfully fetched and saved.")
        else:
            logger_fonction_scrap.error(f"Failed to fetch data from CoinPaprika API. Status code: {response.status_code}")
    except Exception as e:
        logger_fonction_scrap.error(f"An error occurred: {e}")

def process_coins_and_fetch_details():
    """
    Fonction pour lire les données des cryptomonnaies depuis un fichier JSON et récupérer des détails supplémentaires pour chaque cryptomonnaie.
    """
    try:
        with open(coin_list_file, 'r') as json_file:
            coins = json.load(json_file)
        
        for coin in coins:  # Limiter pour cet exemple
            fetch_coin_details(coin['id'], coin['name'], coin['is_active'])
    except FileNotFoundError:
        logger_fonction_scrap.error("File 'coins_data.json' not found. Please run fetch_and_save_coins_data() first.")
    except Exception as e:
        logger_fonction_scrap.error(f"An error occurred: {e}")
