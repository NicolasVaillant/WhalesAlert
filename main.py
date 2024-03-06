import schedule
import time
import requests
import json
import asyncio
import threading
import logging
import os
from pathlib import Path

#----------------------------------------------------
# Coins Tx
#----------------------------------------------------

from resources.python.dynex import dynex
from resources.python.kylacoin import kylacoin
from resources.python.radiant import radiant
from resources.python.lyncoin import lyncoin
from resources.python.fennec import fennec
from resources.python.aipg import aipg
from resources.python.BTCW import BTCW
from resources.python.ferrite import ferrite
from resources.python.bitnet import bitnet
from resources.python.nexa import nexa

from resources.python import table

#----------------------------------------------------
# Scrap CoinMarketCap
#----------------------------------------------------
from resources.python import gainers, losers, trending

#----------------------------------------------------
# Scrap Coins Data
#----------------------------------------------------
from resources.python import coins_data

#----------------------------------------------------
# Logging
#----------------------------------------------------

logger_fonction_scrap = logging.getLogger('scraping')
logger_fonction_scrap.setLevel(logging.INFO)
filenamelog = Path("logs", f"scrap").with_suffix(".log")
handler = logging.FileHandler(filename=filenamelog, encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger_fonction_scrap.addHandler(handler)

logger_fonction_tx_analyze = logging.getLogger('tx_analyze')
if not logger_fonction_tx_analyze.handlers:  # Vérifie s'il y a déjà des handlers configurés
    logger_fonction_tx_analyze.setLevel(logging.INFO)
    filenamelog = Path("logs", "tx_analyze.log")
    handler = logging.FileHandler(filename=filenamelog, encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger_fonction_tx_analyze.addHandler(handler)

logger_fonction_tx_analyze.info("Start")

# Version pc
coins_path_root = Path("resources", "config_python")

# Version serveur
# coins_path_root = Path("/home", "container", "webroot","resources", "config_python")

def dynex_j():
    dynex.job_dynex()
    logger_fonction_tx_analyze.info("End Job Dynex")

def kylacoin_j():
    kylacoin.job_kylacoin()
    logger_fonction_tx_analyze.info("End Job Kylacoin")

def lyncoin_j():
    lyncoin.job_lyncoin()
    logger_fonction_tx_analyze.info("End Job Lyncoin")

def radiant_j():
    radiant.job_radiant()
    logger_fonction_tx_analyze.info("End Job Radiant")

def fennec_j():
    fennec.job_fennec()
    logger_fonction_tx_analyze.info("End Job Fennec")

def aipg_j():
    aipg.job_aipg()
    logger_fonction_tx_analyze.info("End Job AIpg")

def btcw_j():
    BTCW.job_BTCW()
    logger_fonction_tx_analyze.info("End Job BTCW")

def fec_j():
    ferrite.job_ferrite()
    logger_fonction_tx_analyze.info("End Job FEC")

def bit_j():
    bitnet.job_bitnet()
    logger_fonction_tx_analyze.info("End Job BIT")

def nexa_j():
    nexa.job_nexa()
    logger_fonction_tx_analyze.info("End Job NEXA")

def gainer_j():
    asyncio.run(gainers.main())
    logger_fonction_scrap.info("Gainers scrap")

def loser_j():
    asyncio.run(losers.main())
    logger_fonction_scrap.info("Losers scrap")

def trend_j():
    asyncio.run(trending.main())
    logger_fonction_scrap.info("Trendings scrap")

def coins_data_j():
    coins_data.fetch_coins_and_process()
    logger_fonction_scrap.info("Infos coins")

def coins_table_j():
    coin_fetcher = table.CoinFetcher()
    table.update_global_data(coin_fetcher.coins)
    logger_fonction_scrap.info("Infos coins")

threads = {}

def run_threaded(job_func):
    global threads
    func_name = job_func.__name__

    # Vérifier si un thread pour cette fonction est déjà en cours d'exécution
    if func_name in threads and threads[func_name].is_alive():
        return  # Ne pas démarrer un nouveau thread si l'ancien est encore actif

    # Créer et démarrer un nouveau thread
    job_thread = threading.Thread(target=job_func, name=func_name)
    job_thread.start()
    threads[func_name] = job_thread  # Enregistrer la référence du nouveau thread

def all_price ():
    
    coins = ['dynex', 'radiant', 'ai-power-grid', 'kylacoin', 'lyncoin']
    for coin in coins : 
        url: str = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd" #Change to the correct URL for getting RXD price
        try:
            response = requests.get(url)
            data: dict = response.json()
            
            price = data[coin]['usd']
            if coin == "ai-power-grid":
                coin = "aipg"

            coins_path = coins_path_root.joinpath(f"{coin}/tweet.json")
            
            with open(coins_path, "r") as f:
                globals_data = json.load(f)
            f.close()

            globals_data['price'] = price

            with open(coins_path, "w") as f:
                json.dump(globals_data, f, indent=4)

        except Exception as e:
            print(f"Error occurred while getting {coin} price: {e}")

def all_price_paprika ():
    coins = ['fnnc-fennec', 'xrp-xrp', 'fec-ferrite', 'bit-bitnet-io']
    for coin in coins : 
        url: str = f"https://api.coinpaprika.com/v1/tickers/{coin}"
        try:
            response = requests.get(url)
            data: dict = response.json()
            price = data['quotes']['USD']['price']

            path_coin = coin.partition('-')[2].removesuffix("-io")
            
            coins_path = coins_path_root.joinpath(f"{path_coin}/tweet.json")

            with open(coins_path, "r") as f:
                globals_data = json.load(f)
            f.close()

            globals_data['price'] = price

            with open(coins_path, "w") as f:
                json.dump(globals_data, f, indent=4)

        except Exception as e:
            print(f"Error occurred while getting {path_coin} price: {e}")

def all_price_xeggex ():
    path_coin = ''
    ids = ['65ab3039a67290969aecda82']
    for id in ids : 
        url: str = f"https://api.xeggex.com/api/v2/asset/getbyid/{id}"
        try:
            response = requests.get(url)
            data: dict = response.json()
            price = float(data['usdValue'])
            coin = data['ticker']

            path_coin = coin.removesuffix('USDT')

            coins_path = coins_path_root.joinpath(f"{path_coin}/tweet.json")

            with open(coins_path, "r") as f:
                globals_data = json.load(f)
            f.close()

            globals_data['price'] = price

            with open(coins_path, "w") as f:
                json.dump(globals_data, f, indent=4)

        except Exception as e:
            print(f"Error occurred while getting {path_coin} price: {e}")

# Price get
schedule.every(60).minutes.do(all_price)
schedule.every(60).minutes.do(all_price_paprika)
schedule.every(60).minutes.do(all_price_xeggex)

# Scrap CoinMarketCap
schedule.every(60).minutes.do(gainer_j)
schedule.every(60).minutes.do(loser_j)
schedule.every(60).minutes.do(trend_j)

# Scrap Coins Data
schedule.every(1).week.do(coins_data_j)
schedule.every(30).minutes.do(coins_table_j)

# Analyse TX --> THREAD
schedule.every(1).minutes.do(run_threaded, dynex_j)
schedule.every(1).minutes.do(run_threaded, kylacoin_j)
schedule.every(1).minutes.do(run_threaded, lyncoin_j)
schedule.every(1).minutes.do(run_threaded, radiant_j)
schedule.every(1).minutes.do(run_threaded, fennec_j)
schedule.every(1).minutes.do(run_threaded, aipg_j)
schedule.every(1).minutes.do(run_threaded, btcw_j)
schedule.every(1).minutes.do(run_threaded, fec_j)
schedule.every(1).minutes.do(run_threaded, bit_j)
schedule.every(1).minutes.do(run_threaded, nexa_j)

# Exécuter la boucle infiniment
while True:
    schedule.run_pending()
    time.sleep(1)
