import json
import requests
from requests_oauthlib import OAuth1Session
import datetime
import logging
import os
from pathlib import Path
import websocket

# Version pc
tweet_json = Path("resources", "config_python", "warthog", "tweet.json")
config_json = Path("resources", "config_python", "warthog", "config.json")
telegram_json = Path("resources", "config_python", "telegram.json")
tx_data_json = Path("resources", "data_tx", "tx_warthog.json")

# Version serveur
# tweet_json = Path("/home", "container", "webroot","resources", "config_python", "warthog", "tweet.json")
# config_json = Path("/home", "container", "webroot","resources", "config_python", "warthog", "config.json")
# telegram_json = Path("/home", "container", "webroot","resources", "config_python", "telegram.json")
# tx_data_json = Path("/home", "container", "webroot","resources", "data_tx", "tx_warthog.json")

logger_fonction_tx_analyze = logging.getLogger('tx_analyze')
if not logger_fonction_tx_analyze.handlers:  # Vérifie s'il y a déjà des handlers configurés
    logger_fonction_tx_analyze.setLevel(logging.INFO)
    filenamelog = Path("logs", "tx_analyze.log")
    handler = logging.FileHandler(filename=filenamelog, encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger_fonction_tx_analyze.addHandler(handler)

# Charger les valeurs globales initiales
with open(tweet_json, "r") as f:
    globals_data = json.load(f)

last_transaction_value: float = 0.0
last_known_block_index = globals_data.get('last_known_block_index', 0)
tweets_this_day = globals_data.get('tweets_this_day', 0)
day = globals_data.get('day', datetime.datetime.now().day)
post = globals_data.get('post', 0)
price = globals_data.get('price', 0)

def post_tweet(payload: dict) -> None:
    global tweets_this_day
    global day

    # Vérifiez si nous avons commencé un nouveau jour
    if datetime.datetime.now().day != day:
        tweets_this_day = 0
        day = datetime.datetime.now().day

    # Vérifiez si nous avons atteint la limite de tweets pour ce jour
    if tweets_this_day >= 50:
        logger_fonction_tx_analyze.warning("Reached the day limit of tweets.")
        return

    with open(config_json) as f:
        config: dict = json.load(f)
        consumer_key: str = config['CONSUMER_KEY']
        consumer_secret: str = config['CONSUMER_SECRET']
        access_token: str = config['ACCESS_TOKEN']
        access_token_secret: str = config['ACCESS_TOKEN_SECRET']

    # Get request token
    request_token_url: str = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
    except ValueError:
        logger_fonction_tx_analyze.error(
            "There may have been an issue with the consumer_key or consumer_secret you entered."
        )

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    try:
        response = oauth.post("https://api.twitter.com/2/tweets", json=payload)

        if response.status_code != 201:
            raise Exception(f"Request returned an error: {response.status_code} {response.text}")

        tweets_this_day += 1

    except Exception as e:
        logger_fonction_tx_analyze.info(f"Error occurred while posting tweet: {e}")

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
        "message_thread_id" : "2178",
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

# Obtenez le prix de DNX
def get_warthog_price() -> float:
    with open(tweet_json, "r") as f:
        globals_data = json.load(f)
    f.close()
    return globals_data['price'], globals_data['supply']

def on_message(ws, message):
    global tweets_this_day, day, price

    price, circulating_supply = get_warthog_price()
    
    try:
        data = json.loads(message)
        if data.get('type') == 'blockAppend':
            transactions = data.get('data', {}).get('body', {}).get('transfers', [])
            for tx in transactions:
                amount = float(tx.get('amount'))
                if amount > 50: 
                    tx_percentage_of_supply = (amount / float(circulating_supply)) * 100
                    url_tx_hash = "https://wartscan.io/tx/" + tx.get('txHash')

                    total_out_str = human_format(amount)

                    message = "🐋 Whale Alert! 🚨\n"
                    message += f"A transaction of {total_out_str} $WART "
                    message += f"(💵 ${float(price) * amount:.2f}) has been detected. \n"
                    message += f"📊 This represents {tx_percentage_of_supply:.4f}% of the current supply. \n"
                    message += f"🔗 Transaction details: {url_tx_hash}\n"
                    message += "--------------------------------\n"
                    message += "Stay tuned for more updates!\n"
                    message += "https://linktr.ee/whales_alert"

                    payload = {"text": message}

                    print(payload['text'])

                    save_tx(total_out_str,round(float(price) * amount, 2) , round(tx_percentage_of_supply,4), url_tx_hash)

                    # post_tweet(payload)
                    send_telegram_message(payload['text'])

    except json.JSONDecodeError:
        print("Received non-JSON message:", message)

def on_open(ws): 
    print("Connection opened WART")

def start_listening():
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://192.168.1.73:3000/ws/chain_delta",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=lambda ws, error: print("Error:", error),
                                on_close=lambda ws, close_status_code, close_msg: print("### closed ###"))

    ws.run_forever()

def job_warthog() -> None:
    logger_fonction_tx_analyze.info("Job warthog")

    start_listening()