import json
import requests
from requests_oauthlib import OAuth1Session
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path
import websocket
from os import name, system

if name == "nt":
    # Version pc
    telegram_json = Path("resources", "config_python", "telegram.json")
    tx_data_json = Path("resources", "data_tx", "tx_pyrin.json")
    data_coins = Path("resources", "data_coins")
else : 
    # Version serveur
    telegram_json = Path("/home", "container", "config_python", "telegram.json")
    tx_data_json = Path("/home", "container", "webroot","resources", "data_tx", "tx_pyrin.json")
    data_coins = Path("/home", "container", "webroot","resources", "data_coins")

crypto_name = "pyrin"

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

# Fonction pour formater les nombres de manière lisible pour les humains
def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

def send_telegram_message(message):
    with open(telegram_json) as f:
        config: dict = json.load(f)
    url = f"https://api.telegram.org/{config['key']}/sendMessage"
    payload = {
        "chat_id": "-1002081153394",
        "message_thread_id" : "2211",
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

# Obtenez le prix
def get_pyrin_price() -> float:
    crypto_file = Path.joinpath(data_coins, crypto_name + ".json")
    with open(crypto_file, "r") as f:
        globals_data = json.load(f)
    f.close()

    return globals_data['last_price_usd'], globals_data['supply']

def on_message(ws, message):
    price, circulating_supply = get_pyrin_price()
    
    try:
        data = json.loads(message)
        if data.get('type') == 'block':
            block_data = data.get('data', {})
            transactions = block_data.get('transactions', [])

            for tx in transactions:
                amount = float(tx.get('amount'))/pow(10, 8) 
                if amount > 1000000: 
                    tx_percentage_of_supply = (amount / float(circulating_supply)) * 100
                    url_tx_hash = "https://explorer.pyrin.network/block/" + block_data.get('hash', {})

                    total_out_str = human_format(amount)

                    message = "🐋 Whale Alert! 🚨\n"
                    message += f"A transaction of {total_out_str} $PYI "
                    message += f"(💵 ${float(price) * amount:.2f}) has been detected. \n"
                    message += f"📊 This represents {tx_percentage_of_supply:.4f}% of the current supply. \n"
                    message += f"🔗 Transaction details: {url_tx_hash}\n"
                    message += "--------------------------------\n"
                    message += "Stay tuned for more updates!\n"
                    message += "https://linktr.ee/whales_alert"

                    payload = {"text": message}

                    value = round(float(price) * amount, 2)
                    save_tx(total_out_str, value , round(tx_percentage_of_supply,4), url_tx_hash)

                    # send_telegram_message(payload['text'])
            ws.send('')
        if data.get('type') == 'metrics':
            block_data = data.get('data', {})
            circulating_supply = float(block_data.get('circulating', []))/pow(10, 8)
            ws.send('')
        ws.send('')

    except json.JSONDecodeError:
        print("Received non-JSON message:", message)

def on_open(ws): 
    print("Connection opened PYI")
    ws.send(json.dumps({"subscribe": "dashboard"}))
    ws.send(json.dumps({"subscribe": "metrics"}))

def on_error(ws, error):
    logger_fonction_tx_analyze.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### closed PYI ###")
    logger_fonction_tx_analyze.info(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")   
    
def start_listening():
    while True:
        ws = websocket.WebSocketApp("wss://apieco.pyrin.network/",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.run_forever(reconnect=10)
        print("WebSocket disconnected, attempting to reconnect...")


def job_pyrin() -> None:
    logger_fonction_tx_analyze.info("Job Pyrin")

    start_listening()
