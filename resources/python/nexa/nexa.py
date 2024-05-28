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
    tx_data_json = Path("resources", "data_tx", "tx_nexa.json")
    data_coins = Path("resources", "data_coins")
else : 
    # Version serveur
    telegram_json = Path("/home", "container", "config_python", "telegram.json")
    tx_data_json = Path("/home", "container", "webroot","resources", "data_tx", "tx_nexa.json")
    data_coins = Path("/home", "container", "webroot","resources", "data_coins")

crypto_name = "nexa"

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
def get_nexa_price() -> float:
    crypto_file = Path.joinpath(data_coins, crypto_name + ".json")
    with open(crypto_file, "r") as f:
        globals_data = json.load(f)
    f.close()

    return globals_data['last_price_usd']

# Récupérez les informations sur les transactions
def get_transaction_info():
    global seen_transactions  # Ajout de la variable globale

    # Get the total circulating supply
    supply_url: str = "https://www.coinexplorer.net/api/v1/NEXA/circulationSupply"
    try:
        supply_response = requests.get(supply_url)
        supply_data = supply_response.json()
        circulating_supply = float(supply_data)

        url: str = "https://www.coinexplorer.net/api/v1/NEXA/getblockcount"
        url_block : str = "https://www.coinexplorer.net/api/v1/NEXA/block?height="
        url_tx: str = "https://explorer.nexa.org/block/"
        data = requests.get(url)
        block_height = data.json()

        block_data = requests.get(url_block + str(block_height))
        block_data_json = block_data.json()

        block_hash = block_data_json['result']['hash']

        transactions = []
        
        for tx in block_data_json['result']['tx']:
            if tx not in seen_transactions:  # Check if we've seen this transaction
                tx_outputs = requests.get(f"https://www.coinexplorer.net/api/v1/NEXA/transaction?txid={tx}")
                tx_outputs_json = tx_outputs.json()
                for tx_output in tx_outputs_json['result']['vout']:
                    amount: float = float(tx_output['value'])
                    if amount > 5000000:
                        tx_percentage_of_supply: float = (amount / circulating_supply) * 100
                        transactions.append((amount, tx_percentage_of_supply, url_tx + block_hash))
                seen_transactions.add(tx)  # Add the transaction hash to our set of seen transactions
        return transactions
    
    except Exception as e:
        logger_fonction_tx_analyze.error(f"Error occurred while getting transaction info: {e}")
        return []

def send_telegram_message(message):
    with open(telegram_json) as f:
        config: dict = json.load(f)
    url = f"https://api.telegram.org/{config['key']}/sendMessage"
    payload = {
        "chat_id": "-1002081153394",
        "message_thread_id" : "1387",
        "text": message
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

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

def job_nexa() -> None:
    logger_fonction_tx_analyze.info("Job nexa")

    # Récupérez le prix NEXA
    price: float = get_nexa_price()

    # Récupérez les informations sur les transactions
    transactions = get_transaction_info()

    for transaction in transactions:
        total_out, tx_percentage_of_supply, url_tx_hash = transaction

        total_out_str = human_format(total_out)

        message = "🐋 Whale Alert! 🚨\n"
        message += f"A transaction of {total_out_str} $NEXA "
        message += f"(💵 ${float(price) * total_out:.2f}) has been detected. \n"
        message += f"📊 This represents {tx_percentage_of_supply:.4f}% of the current supply. \n"
        message += f"🔗 Transaction details: {url_tx_hash}\n"
        message += "--------------------------------\n"
        message += "Stay tuned for more updates!\n"
        message += "https://linktr.ee/whales_alert"

        payload = {"text": message}

        value = round(float(price) * total_out, 2)
        save_tx(total_out_str, value , round(tx_percentage_of_supply,4), url_tx_hash)

        send_telegram_message(payload['text'])