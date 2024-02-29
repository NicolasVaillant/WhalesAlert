import json
import requests
from requests_oauthlib import OAuth1Session
import datetime
import logging
from pathlib import Path
import os

logger_fonction_tx_analyze = logging.getLogger('tx_analyze')
if not logger_fonction_tx_analyze.handlers:  # Vérifie s'il y a déjà des handlers configurés
    logger_fonction_tx_analyze.setLevel(logging.INFO)
    filenamelog = Path("log", "tx_analyze.log")
    handler = logging.FileHandler(filename=filenamelog, encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger_fonction_tx_analyze.addHandler(handler)


# Charger les valeurs globales initiales
with open("./resources/config_python/ferrite/tweet.json", "r") as f:
    globals_data = json.load(f)

last_transaction_value: float = 0.0
last_known_block_index = globals_data.get('last_known_block_index', 0)
tweets_this_day = globals_data.get('tweets_this_day', 0)
day = globals_data.get('day', datetime.datetime.now().day)
post = globals_data.get('post', 0)

# Variable globale pour les transactions déjà vues
seen_transactions: set = set()

# Obtenez le prix de ferrite
def get_fec_price() -> float:
    with open("./resources/config_python/ferrite/tweet.json", "r") as f:
        globals_data = json.load(f)
    f.close()

    return globals_data['price']

# Récupérez les informations sur les transactions
def get_transaction_info():
    global last_transaction_value
    global last_known_block_index
    global seen_transactions  # Ajout de la variable globale

    # Get the total circulating supply
    supply_url: str = "https://ferritecoin.org:53443/ext/getmoneysupply"
    try:
        supply_response = requests.get(supply_url)
        supply_data = supply_response.text
        circulating_supply = float(supply_data)

        url: str = "https://ferritecoin.org:53443/api/getblockcount"
        url_block_hash = "https://ferritecoin.org:53443/api/getblockhash?index="
        url_block : str = "https://ferritecoin.org:53443/api/getblock?hash="
        url_tx: str = "https://ferritecoin.org:53443/tx/"
        data = requests.get(url)
        block_heigh = data.json()

        block_hash_j = requests.get(f"https://ferritecoin.org:53443/api/getblockhash?index={block_heigh}")
        url_block_json = block_hash_j.json()

        data_block = requests.get(f"{url_block}{url_block_json}")
        data_json = data_block.json()
        transactions = []
        
        for tx in data_json['tx']:
            if tx not in seen_transactions:  # Check if we've seen this transaction
                tx_get = requests.get(f'https://ferritecoin.org:53443/api/getrawtransaction?txid={tx}&decrypt=1')
                tx_get_json = tx_get.json()
                for tx_output in tx_get_json['vout']:
                    if tx_output['scriptPubKey']['type'] != "witness_mweb_hogaddr" :
                        amount: float = float(tx_output['value'])
                        if amount > 50000:
                            tx_percentage_of_supply: float = (amount / circulating_supply) * 100
                            transactions.append((amount, tx_percentage_of_supply, url_tx + tx))
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

    with open("./resources/config_python/ferrite/config.json") as f:
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
        logger_fonction_tx_analyze.error(f"Error occurred while posting tweet: {e}")

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
        "message_thread_id" : "1127",
        "text": message,
    }
    
    response = requests.post(url, data=payload)
    return response.json()

def save_tx(total_out, value, tx_percentage_of_supply, url_tx_hash):
    # Chemin du dossier où stocker les transactions
    transactions_dir_path = './resources/data_tx'
    # Nom du fichier JSON pour stocker les transactions
    transactions_file_name = 'tx_ai_power_grid.json'
    # Chemin complet du fichier
    transactions_file_path = os.path.join(transactions_dir_path, transactions_file_name)
    
    # S'assurer que le dossier existe, sinon le créer
    os.makedirs(transactions_dir_path, exist_ok=True)
    
    # Essayer de lire les transactions existantes, sinon initialiser une liste vide
    try:
        with open(transactions_file_path, 'r') as file:
            transactions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        transactions = []

    # Créer un dictionnaire pour la nouvelle transaction
    new_transaction = {
        'total_out': total_out,
        'value': value,
        'porcentage_supply': tx_percentage_of_supply,
        'url_tx_hash': url_tx_hash,
        'date': datetime.datetime.now().isoformat()  # Ajouter un horodatage pour la transaction
    }

    # Insérer la nouvelle transaction au début de la liste
    transactions.insert(0, new_transaction)

    # Sauvegarder la liste mise à jour dans le fichier JSON
    with open(transactions_file_path, 'w') as file:
        json.dump(transactions, file, indent=4)

def job_ferrite() -> None:
    global tweets_this_day, day
    logger_fonction_tx_analyze.info("Job FEC")

    with open("./resources/config_python/ferrite/tweet.json", "r") as f:
        globals_data = json.load(f)

    # Récupérez le prix FEC
    price: float = get_fec_price()

    # Récupérez les informations sur les transactions
    transactions = get_transaction_info()

    for transaction in transactions:
        total_out, tx_percentage_of_supply, url_tx_hash = transaction
        total_out_str = human_format(total_out)

        message = "🐋 Whale Alert! 🚨\n"
        message += f"A transaction of {total_out_str} $FEC "
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

    with open("./resources/config_python/ferrite/tweet.json", "w") as f:
        json.dump(globals_data, f, indent=4)
