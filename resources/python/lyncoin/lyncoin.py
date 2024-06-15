import json
import requests
from requests_oauthlib import OAuth1Session
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path
from os import name, system

if name == "nt":
    # Version pc
    tweet_json = Path("resources", "config_python", "lyncoin", "tweet.json")
    config_json = Path("resources", "config_python", "lyncoin", "config.json")
    telegram_json = Path("resources", "config_python", "telegram.json")
    tx_data_json = Path("resources", "data_tx", "tx_lyncoin.json")
    data_coins = Path("resources", "data_coins")
else :
    # Version serveur
    tweet_json = Path("/home", "container", "webroot","resources", "config_python", "lyncoin", "tweet.json")
    config_json = Path("/home", "container", "config_python", "lyncoin", "config.json")
    telegram_json = Path("/home", "container", "config_python", "telegram.json")
    tx_data_json = Path("/home", "container", "webroot","resources", "data_tx", "tx_lyncoin.json")
    data_coins = Path("/home", "container", "webroot","resources", "data_coins")

crypto_name = "lyncoin"

logger_fonction_tx_analyze = logging.getLogger('tx_analyze')
if not logger_fonction_tx_analyze.handlers:
    logger_fonction_tx_analyze.setLevel(logging.INFO)
    filenamelog = Path("logs", "tx_analyze.log")
    handler = TimedRotatingFileHandler(filenamelog, when='midnight', interval=1, backupCount=7, encoding='utf-8')
    handler.suffix = "%Y-%m-%d"  # suffixe le fichier de log avec la date du jour
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger_fonction_tx_analyze.addHandler(handler)

# Charger les valeurs globales initiales
with open(tweet_json, "r") as f:
    globals_data = json.load(f)

tweets_this_day = globals_data.get('tweets_this_day', 0)
day = globals_data.get('day', datetime.datetime.now().day)

# Variable globale pour les transactions déjà vues
seen_transactions: set = set()

# Obtenez le prix
def get_lyncoin_price() -> float:
    crypto_file = Path.joinpath(data_coins, crypto_name + ".json")
    with open(crypto_file, "r") as f:
        globals_data = json.load(f)
    f.close()

    return globals_data['last_price_usd']

# Récupérez les informations sur les transactions
def get_transaction_info():
    global seen_transactions  # Ajout de la variable globale

    # Get the total circulating supply
    supply_url: str = "https://api.lcnxp.com/supply"
    try:
        supply_response = requests.get(supply_url)
        supply_data: dict = supply_response.json()
        circulating_supply: float = float(supply_data['result']['circulating'])

        url: str = "https://api.lcnxp.com/blocks?offset=0&limit=10"
        url_block : str = "https://api.lcnxp.com/txs?block="
        url_tx: str = "https://lcnxp.com/block/"
        data = requests.get(url)
        data_json: dict = data.json()

        transactions = []
        
        for block in data_json['result']:
            block_hash = block['hash']
            block_data = requests.get(url_block + block_hash)
            block_data_json = block_data.json()
            for tx in block_data_json['result']:
                if tx['hash'] not in seen_transactions:  # Check if we've seen this transaction
                    for tx_output in tx['outputs']:
                        amount: float = float(tx_output['value'])
                        if amount > 50000000:
                            tx_percentage_of_supply: float = (amount / circulating_supply) * 100
                            transactions.append((amount, tx_percentage_of_supply, url_tx + block_hash))
                    seen_transactions.add(tx['hash'])  # Add the transaction hash to our set of seen transactions

        return transactions
    
    except Exception as e:
        logger_fonction_tx_analyze.error(f"Error occurred while getting transaction info: {e}")
        return []

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
        "message_thread_id" : "246",
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

def job_lyncoin() -> None:
    global tweets_this_day, day
    logger_fonction_tx_analyze.info("Job Lyncoin")

    with open(tweet_json, "r") as f:
        globals_data = json.load(f)

    # Récupérez le prix DNX
    price: float = get_lyncoin_price()

    # Récupérez les informations sur les transactions
    transactions = get_transaction_info()

    for transaction in transactions:
        total_out, tx_percentage_of_supply, url_tx_hash = transaction
        total_out_str = human_format(total_out)

        message = "🐋 Whale Alert! 🚨\n"
        message += f"A transaction of {total_out_str} $LCN "
        message += f"(💵 ${float(price) * total_out:.2f}) has been detected. \n"
        message += f"📊 This represents {tx_percentage_of_supply:.4f}% of the current supply. \n"
        message += f"🔗 Transaction details: {url_tx_hash}\n"
        message += "--------------------------------\n"
        message += "Stay tuned for more updates!\n"
        message += "https://linktr.ee/whales_alert"

        payload = {"text": message}

        value = round(float(price) * total_out, 2)
        save_tx(total_out_str, value , round(tx_percentage_of_supply,4), url_tx_hash)

        # post_tweet(payload)
        # send_telegram_message(payload['text'])

    # Sauvegarder les valeurs globales après les modifications
    globals_data['tweets_this_day'] = tweets_this_day
    globals_data['day'] = day

    with open(tweet_json, "w") as f:
        json.dump(globals_data, f, indent=4)
