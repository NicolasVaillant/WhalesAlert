import json
import requests
from requests_oauthlib import OAuth1Session
import datetime
from pathlib import Path
import logging
import os

# Version pc
tweet_json = Path("resources", "config_python", "fennec", "tweet.json")
config_json = Path("resources", "config_python", "fennec", "config.json")
telegram_json = Path("resources", "config_python", "fennec", "telegram.json")
tx_data_json = Path("resources", "data_tx", "tx_fennec.json")

# Version serveur
# tweet_json = Path("/home", "container", "webroot","resources", "config_python", "fennec", "tweet.json")
# config_json = Path("/home", "container", "webroot","resources", "config_python", "fennec", "config.json")
# telegram_json = Path("/home", "container", "webroot","resources", "config_python", "fennec", "telegram.json")
# tx_data_json = Path("/home", "container", "webroot","resources", "data_tx", "tx_fennec.json")

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

# Variable globale pour les transactions déjà vues
seen_transactions: set = set()

# Obtenez le prix de DNX
def get_fennec_price() -> float:
    with open(tweet_json, "r") as f:
        globals_data = json.load(f)
    f.close()

    return globals_data['price']

# Récupérez les informations sur les transactions
def get_transaction_info():
    global last_transaction_value
    global last_known_block_index
    global seen_transactions  # Ajout de la variable globale

    # Get the total circulating supply
    supply_url: str = "https://scan.fennecblockchain.com/ext/getmoneysupply"
    try:
        supply_response = requests.get(supply_url)
        supply_data = supply_response.json()
        circulating_supply = float(supply_data)

        url: str = "https://scan.fennecblockchain.com/ext/getlasttxs/5/0/5"
        url_block : str = "https://scan.fennecblockchain.com/api/getblock?hash="
        url_tx: str = "https://scan.fennecblockchain.com/block/"
        data = requests.get(url)
        data_json: dict = data.json()

        transactions = []
        
        for block in data_json:
            block_hash = block['blockhash']
            block_data = requests.get(url_block + block_hash)
            block_data_json = block_data.json()

            for tx in block_data_json['tx']:
                if tx not in seen_transactions:  # Check if we've seen this transaction
                    tx_outputs = requests.get(f"https://scan.fennecblockchain.com/api/getrawtransaction?txid={tx}&decrypt=1")
                    tx_outputs_json = tx_outputs.json()
                    for tx_output in tx_outputs_json['vout']:
                        amount: float = float(tx_output['value'])
                        if amount > 10000:
                            tx_percentage_of_supply: float = (amount / circulating_supply) * 100
                            transactions.append((amount, tx_percentage_of_supply, url_tx + block_hash))
                            last_transaction_value = amount
                    seen_transactions.add(tx)  # Add the transaction hash to our set of seen transactions
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

def send_telegram_message(message):
    with open(telegram_json) as f:
        config: dict = json.load(f)
    url = f"https://api.telegram.org/{config['key']}/sendMessage"
    payload = {
        "chat_id": "-1002081153394",
        "message_thread_id" : "251",
        "text": message
    }
    response = requests.post(url, data=payload)
    return response.json()

def save_tx(total_out, value, tx_percentage_of_supply, url_tx_hash):

    # S'assurer que le dossier existe, sinon le créer
    os.makedirs(tx_data_json, exist_ok=True)
    
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

def job_fennec() -> None:
    global tweets_this_day, day
    logger_fonction_tx_analyze.info("Job Fennec")

    with open(tweet_json, "r") as f:
        globals_data = json.load(f)

    # Récupérez le prix FNNC
    price: float = get_fennec_price()

    # Récupérez les informations sur les transactions
    transactions = get_transaction_info()

    for transaction in transactions:
        total_out, tx_percentage_of_supply, url_tx_hash = transaction

        total_out_str = human_format(total_out)

        message = "🐋 Whale Alert! 🚨\n"
        message += f"A transaction of {total_out_str} $FNNC "
        message += f"(💵 ${float(price) * total_out:.2f}) has been detected. \n"
        message += f"📊 This represents {tx_percentage_of_supply:.4f}% of the current supply. \n"
        message += f"🔗 Transaction details: {url_tx_hash}\n"
        message += "--------------------------------\n"
        message += "Stay tuned for more updates!\n"
        message += "https://linktr.ee/whales_alert"

        payload = {"text": message}
        save_tx(total_out_str,(float(price) * total_out) , tx_percentage_of_supply, url_tx_hash)

        # post_tweet(payload)
        send_telegram_message(payload['text'])

    # Sauvegarder les valeurs globales après les modifications
    globals_data['last_known_block_index'] = last_known_block_index
    globals_data['tweets_this_day'] = tweets_this_day
    globals_data['day'] = day

    with open(tweet_json, "w") as f:
        json.dump(globals_data, f, indent=4)
