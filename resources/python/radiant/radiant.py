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
    tweet_json = Path("resources", "config_python", "radiant", "tweet.json")
    config_json = Path("resources", "config_python", "radiant", "config.json")
    telegram_json = Path("resources", "config_python", "telegram.json")
    tx_data_json = Path("resources", "data_tx", "tx_radiant.json")
    data_coins = Path("resources", "data_coins")
else : 
    # Version serveur
    tweet_json = Path("/home", "container", "webroot","resources", "config_python", "radiant", "tweet.json")
    config_json = Path("/home", "container", "config_python", "radiant", "config.json")
    telegram_json = Path("/home", "container", "config_python", "telegram.json")
    tx_data_json = Path("/home", "container", "webroot","resources", "data_tx", "tx_radiant.json")
    data_coins = Path("/home", "container", "webroot","resources", "data_coins")

crypto_name = "radiant"

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

# Initialiser les variables globales
last_known_block_index = globals_data.get('last_known_block_index', 0)
tweets_this_day = globals_data.get('tweets_this_day', 0)
day = globals_data.get('day', datetime.datetime.now().day)

# Obtenez le prix
def get_radiant_price() -> float:
    crypto_file = Path.joinpath(data_coins, crypto_name + ".json")
    with open(crypto_file, "r") as f:
        globals_data = json.load(f)
    f.close()

    return globals_data['last_price_usd']

# Get the money supply
def get_money_supply() -> float:
    url: str = "https://radiantexplorer.com/ext/getbasicstats"
    try:
        response = requests.get(url)
        data: dict = response.json()
        return data['money_supply']
    except Exception as e:
        logger_fonction_tx_analyze.error(f"Error occurred while getting Radiant supply: {e}")
        return 0.0

# Fonction pour obtenir les informations de transaction
def get_transaction_info(money_supply: float) -> list:
    global last_known_block_index

    url = "https://radiantexplorer.com/ext/getlasttxs/100/0/100"
    try:
        response = requests.get(url)
        transactions_data = response.json()
        transaction_list = []

        for transaction in transactions_data:
            block_index = transaction['blockindex']
            
            # Si le block index est déjà connu, on continue la boucle
            if block_index <= last_known_block_index:
                continue

            output_amount = float(transaction['amount'])

            # Si la transaction est supérieure à un certain montant, elle est considérée
            if output_amount > 10000000.0:
                percentage_of_total_supply = (output_amount / money_supply) * 100
                transaction_list.append((output_amount, transaction['txid'], percentage_of_total_supply))
                # Mettre à jour last_known_block_index pour le nouveau bloc
                last_known_block_index = block_index

        return transaction_list
    except Exception as e:
        logger_fonction_tx_analyze.error(f"Error occurred while getting transaction info: {e}")
        return []

# Fonction pour poster un tweet
def post_tweet(payload: dict) -> None:
    global tweets_this_day
    global day

    # Vérifier si un nouveau jour a commencé
    if datetime.datetime.now().day != day:
        tweets_this_day = 0
        day = datetime.datetime.now().day

    # Vérifier si la limite quotidienne est atteinte
    if tweets_this_day >= 50:
        logger_fonction_tx_analyze.warning("Reached the daily limit of tweets.")
        return

    # Charger les informations d'authentification
    with open(config_json) as f:
        config = json.load(f)

    # Authentification OAuth1 avec Twitter
    oauth = OAuth1Session(
        client_key=config['CONSUMER_KEY'],
        client_secret=config['CONSUMER_SECRET'],
        resource_owner_key=config['ACCESS_TOKEN'],
        resource_owner_secret=config['ACCESS_TOKEN_SECRET']
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
    with open(telegram_json) as f:
        config: dict = json.load(f)
    url = f"https://api.telegram.org/{config['key']}/sendMessage"
    payload = {
        "chat_id": "-1002081153394",
        "message_thread_id" : "6",
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

# Tâche planifiée pour exécuter la routine
def job_radiant():
    global last_known_block_index
    global tweets_this_day
    global day
    logger_fonction_tx_analyze.info("Job Radiant")

    with open(tweet_json, "r") as f:
        globals_data = json.load(f)

    # Obtenir le prix et l'offre monétaire
    price = get_radiant_price()
    money_supply = get_money_supply()

    # Obtenir et traiter les informations de transaction
    transactions = get_transaction_info(money_supply)

    for total_out, txid, tx_percentage_of_supply in transactions:
        total_out_str = human_format(total_out)
        url_tx_hash = f"https://radiantexplorer.com/tx/{txid}"

        message = "🐋 Whale Alert! 🚨\n"
        message += f"A transaction of {total_out_str} $RXD "
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

    # Sauvegarder les valeurs globales
    globals_data['last_known_block_index'] = last_known_block_index
    globals_data['tweets_this_day'] = tweets_this_day
    globals_data['day'] = day

    # Écrire dans le fichier json
    with open(tweet_json, "w") as f:
        json.dump(globals_data, f, indent=4)