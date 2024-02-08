import schedule
import time
from os import name, system
import requests
import json
import asyncio
import os
import threading
import logging
from pathlib import Path

#-----------------------------
# Coins

# from dynex import dynex
# from kylacoin import kylacoin
# from radiant import radiant
# from lyncoin import lyncoin
# from fennec import fennec
# from xrp import xrp
# from aipg import aipg
# from BTCW import BTCW
# from ferrite import ferrite
# from Bitnet import Bitnet
# from nexa import nexa

#------------------------------------
# Scrap CoinMarketCap

from resources.python import gainers, losers, trending

#----------------------------------------------------
# Logging

logger_fonction = logging.getLogger('scraping')
logger_fonction.setLevel(logging.INFO)
filenamelog = Path("log", f"scrap").with_suffix(".log")
handler = logging.FileHandler(filename=filenamelog, encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger_fonction.addHandler(handler)

clear, back_slash = "clear", "/"
if name == "nt":
    clear, back_slash = "cls", "\\"
system(clear)

print("Start")

# def dynex_j():
#     dynex.job_dynex()
#     print("End Job Dynex")

# def kylacoin_j():
#     kylacoin.job_kylacoin()
#     print("End Job Kylacoin")

# def lyncoin_j():
#     lyncoin.job_lyncoin()
#     print("End Job Lyncoin")

# def radiant_j():
#     radiant.job_radiant()
#     print("End Job Radiant")

# def fennec_j():
#     fennec.job_fennec()
#     print("End Job Fennec")

# def xrp_j():
#     xrp.job_xrp()
#     print("End Job Ripple")

# def aipg_j():
#     aipg.job_aipg()
#     print("End Job AIpg")

# def btcw_j():
#     BTCW.job_BTCW()
#     print("End Job BTCW")

# def fec_j():
#     ferrite.job_ferrite()
#     print("End Job FEC")

# def bit_j():
#     Bitnet.job_bitnet()
#     print("End Job BIT")

# def nexa_j():
#     nexa.job_nexa()
#     print("End Job NEXA")

def gainer_j():
    asyncio.run(gainers.main())
    logger_fonction.info("Gainers scrap")

def loser_j():
    asyncio.run(losers.main())
    logger_fonction.info("Losers scrap")

def trend_j():
    asyncio.run(trending.main())
    logger_fonction.info("Trendings scrap")

# def display_prices():
#     config_path = "./config/"
#     for item in os.listdir(config_path):
#         item_path = os.path.join(config_path, item)
#         # Vérifier si l'élément est un dossier
#         if os.path.isdir(item_path):
#             try:
#                 with open(os.path.join(item_path, "tweet.json"), "r") as file:
#                     data = json.load(file)
#                     # Assumer que le nom du dossier est le même que l'ID de la monnaie
#                     coin_id = item
#                     print(f"{coin_id.upper()} Price: {data.get('price', 'N/A')}")
#             except Exception as e:
#                 print(f"Could not read price for {item}: {e}")
#         else:
#             # Ignorer les fichiers qui ne sont pas des dossiers
#             continue

# def command_listener():
#     while True:
#         cmd = input("Enter command: ")
#         if cmd == "/price":
#             display_prices()

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

# def all_price ():
    
#     coins = ['dynex', 'radiant', 'ai-power-grid', 'kylacoin', 'lyncoin']
#     for coin in coins : 
#         url: str = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd" #Change to the correct URL for getting RXD price
#         try:
#             response = requests.get(url)
#             data: dict = response.json()
            
#             price = data[coin]['usd']
#             if coin == "ai-power-grid":
#                 coin = "aipg"
            
#             with open(f"./config/{coin}/tweet.json", "r") as f:
#                 globals_data = json.load(f)
#             f.close()

#             globals_data['price'] = price

#             with open(f"./config/{coin}/tweet.json", "w") as f:
#                 json.dump(globals_data, f, indent=4)

#         except Exception as e:
#             print(f"Error occurred while getting {coin} price: {e}")

# def all_price_paprika ():
#     path_coin = ''
#     coins = ['fnnc-fennec', 'xrp-xrp', 'fec-ferrite', 'bit-bitnet-io']
#     for coin in coins : 
#         url: str = f"https://api.coinpaprika.com/v1/tickers/{coin}"
#         try:
#             response = requests.get(url)
#             data: dict = response.json()
#             price = data['quotes']['USD']['price']

#             path_coin = coin.partition('-')[2].removesuffix("-io")

#             with open(f"./config/{path_coin}/tweet.json", "r") as f:
#                 globals_data = json.load(f)
#             f.close()

#             globals_data['price'] = price

#             with open(f"./config/{path_coin}/tweet.json", "w") as f:
#                 json.dump(globals_data, f, indent=4)

#         except Exception as e:
#             print(f"Error occurred while getting {path_coin} price: {e}")

# def all_price_xeggex ():
#     path_coin = ''
#     ids = ['65ab3039a67290969aecda82']
#     for id in ids : 
#         url: str = f"https://api.xeggex.com/api/v2/asset/getbyid/{id}"
#         try:
#             response = requests.get(url)
#             data: dict = response.json()
#             price = float(data['usdValue'])
#             coin = data['ticker']

#             path_coin = coin.removesuffix('USDT')

#             with open(f"./config/{path_coin}/tweet.json", "r") as f:
#                 globals_data = json.load(f)
#             f.close()

#             globals_data['price'] = price

#             with open(f"./config/{path_coin}/tweet.json", "w") as f:
#                 json.dump(globals_data, f, indent=4)

#         except Exception as e:
#             print(f"Error occurred while getting {path_coin} price: {e}")


# Price get
# schedule.every(30).minutes.do(all_price)
# schedule.every(30).minutes.do(all_price_paprika)
# schedule.every(30).minutes.do(all_price_xeggex)

# Scrap CoinMarketCap
schedule.every(30).minutes.do(gainer_j)
schedule.every(30).minutes.do(loser_j)
schedule.every(30).minutes.do(trend_j)

# listener_thread = threading.Thread(target=command_listener, daemon=True)
# listener_thread.start()

# Analyse TX --> THREAD
# schedule.every(60).seconds.do(run_threaded, dynex_j)
# schedule.every(60).seconds.do(run_threaded, kylacoin_j)
# schedule.every(60).seconds.do(run_threaded, lyncoin_j)
# schedule.every(60).seconds.do(run_threaded, radiant_j)
# schedule.every(60).seconds.do(run_threaded, fennec_j)
# schedule.every(60).seconds.do(run_threaded, xrp_j)
# schedule.every(60).seconds.do(run_threaded, aipg_j)
# schedule.every(60).seconds.do(run_threaded, btcw_j)
# schedule.every(60).seconds.do(run_threaded, fec_j)
# schedule.every(60).seconds.do(run_threaded, bit_j)
# schedule.every(60).seconds.do(run_threaded, nexa_j)

# Exécuter la boucle infiniment
while True:
    schedule.run_pending()
    time.sleep(1)
