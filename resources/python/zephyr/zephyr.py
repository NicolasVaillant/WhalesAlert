import json
import requests
from requests_oauthlib import OAuth1Session
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import os
from os import name, system

if name == "nt":
    # Version pc
    telegram_json = Path("resources", "config_python", "telegram.json")
    tx_data_json = Path("resources", "data_tx", "tx_zephyr.json")
    data_coins = Path("resources", "data_coins")
else :
    # Version serveur
    telegram_json = Path("/home", "container", "config_python", "telegram.json")
    tx_data_json = Path("/home", "container", "webroot","resources", "data_tx", "tx_zephyr.json")
    data_coins = Path("/home", "container", "webroot","resources", "data_coins")

crypto_name = "zephyr_protocol"

logger_fonction_tx_analyze = logging.getLogger('tx_analyze')
if not logger_fonction_tx_analyze.handlers:
    logger_fonction_tx_analyze.setLevel(logging.INFO)
    filenamelog = Path("logs", "tx_analyze.log")
    handler = TimedRotatingFileHandler(filenamelog, when='midnight', interval=1, backupCount=7, encoding='utf-8')
    handler.suffix = "%Y-%m-%d"  # suffixe le fichier de log avec la date du jour
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger_fonction_tx_analyze.addHandler(handler)

# Variable globale pour les transactions déjà vues
seen_transactions: set = set()

# Obtenez le prix
def get_zephyr_price() -> float:
    crypto_file = Path.joinpath(data_coins, crypto_name + ".json")
    with open(crypto_file, "r") as f:
        globals_data = json.load(f)
    f.close()

    return globals_data['last_price_usd']

# Récupérez les informations sur les transactions
def get_transaction_info():
    global seen_transactions  # Ajout de la variable globale

    # Get the total circulating supply
    supply_url: str = "https://explorer.zephyrprotocol.com/api/supply"
    url_tx = "https://explorer.zephyrprotocol.com/tx/"
    try:
        supply_response = requests.get(supply_url)
        supply_data = supply_response.json()
        circulating_supply = float(supply_data['ZEPH'])

        url: str = "https://explorer.zephyrprotocol.com/api/transactions"

        data_block = requests.get(url)
        data_json = data_block.json()

        transactions = []
        
        for tx in data_json['data']['blocks']:
            for txs in tx['txs']:
                tx_hash = txs['tx_hash']
                if tx_hash not in seen_transactions:
                    tx_get = requests.get(f'https://explorer.zephyrprotocol.com/api/transaction/{tx_hash}')
                    tx_get_json = tx_get.json()
                    for detail_tx in tx_get_json['data']['outputs']:
                        amount = float(detail_tx['amount'])/10**12
                        if amount > 1000:
                            tx_percentage_of_supply: float = (amount / circulating_supply) * 100
                            transactions.append((amount, tx_percentage_of_supply, url_tx + tx_hash))
                        seen_transactions.add(tx_hash)  # Add the transaction hash to our set of seen transactions
        return transactions
    
    except Exception as e:
        logger_fonction_tx_analyze.error(f"Error occurred while getting transaction info: {e}")
        return []

# Fonction pour formater les nombres de manière lisible pour les humains
def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

def send_telegram_message(message):
    with open("./resources/config_python/telegram.json") as f:
        config: dict = json.load(f)
    url = f"https://api.telegram.org/{config['key']}/sendMessage"
    
    payload = {
        "chat_id": "-1002081153394",
        "message_thread_id" : "3673",
        "text": message,
    }
    
    response = requests.post(url, data=payload)
    return response.json()

def save_tx(total_out, value, tx_percentage_of_supply, url_tx_hash):

    # S'assurer que le dossier existe, sinon le créer
    directory = os.path.dirname(tx_data_json)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    # Essayer de lire les transactions existantes, sinon initialiser une liste vide
    try:
        with open(tx_data_json, 'r') as file:
            transactions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        transactions = []

    # Créer un dictionnaire pour la nouvelle transaction
    new_transaction = {
        'amount': total_out,
        'value': value,
        'porcentage_supply': tx_percentage_of_supply,
        'url': url_tx_hash,
        'date': datetime.datetime.now().isoformat()  # Ajouter un horodatage pour la transaction
    }

    # Insérer la nouvelle transaction au début de la liste
    transactions.insert(0, new_transaction)

    # Sauvegarder la liste mise à jour dans le fichier JSON
    with open(tx_data_json, 'w') as file:
        json.dump(transactions, file, indent=4)

def job_zephyr():
    global tweets_this_day, day
    logger_fonction_tx_analyze.info("Job ZEPH")

    price: float = get_zephyr_price()

    # Récupérez les informations sur les transactions
    transactions = get_transaction_info()

    for transaction in transactions:
        total_out, tx_percentage_of_supply, url_tx_hash = transaction
        total_out_str = human_format(total_out)

        message = "🐋 Whale Alert! 🚨\n"
        message += f"A transaction of {total_out_str} $ZEPH "
        message += f"(💵 ${float(price) * total_out:.2f}) has been detected. \n"
        message += f"📊 This represents {tx_percentage_of_supply:.4f}% of the current supply. \n"
        message += f"🔗 Transaction details: {url_tx_hash}\n"
        message += "--------------------------------\n"
        message += "Stay tuned for more updates!\n"
        message += "https://linktr.ee/whales_alert"

        payload = {"text": message}

        value = round(float(price) * total_out, 2)
        save_tx(total_out_str, value , round(tx_percentage_of_supply,4), url_tx_hash)

        # send_telegram_message(payload['text'])
