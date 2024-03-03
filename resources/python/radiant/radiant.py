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
with open("./resources/config_python/radiant/tweet.json", "r") as f:
    globals_data = json.load(f)

# Initialiser les variables globales
last_transaction_value = globals_data.get('last_transaction_value', 0.0)
last_known_block_index = globals_data.get('last_known_block_index', 0)
tweets_this_day = globals_data.get('tweets_this_day', 0)
day = globals_data.get('day', datetime.datetime.now().day)
post = globals_data.get('post', 0)

# Get the price of RXD
def get_radiant_price() -> float:
    with open("./resources/config_python/radiant/tweet.json", "r") as f:
        globals_data = json.load(f)
    f.close()
    return globals_data['price']

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
    global last_transaction_value
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
                last_transaction_value = output_amount
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
    with open("./resources/config_python/radiant/config.json") as f:
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
    with open("./resources/config_python/telegram.json") as f:
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
# Tâche planifiée pour exécuter la routine
def job_radiant():
    global last_known_block_index
    global tweets_this_day
    global day
    logger_fonction_tx_analyze.info("Job Radiant")

    with open("./resources/config_python/radiant/tweet.json", "r") as f:
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
        
        save_tx(total_out_str,(float(price) * total_out) , tx_percentage_of_supply, url_tx_hash)

        post_tweet(payload)
        send_telegram_message(payload['text'])

    # Sauvegarder les valeurs globales
    globals_data['last_known_block_index'] = last_known_block_index
    globals_data['tweets_this_day'] = tweets_this_day
    globals_data['day'] = day

    # Écrire dans le fichier json
    with open("./resources/config_python/radiant/tweet.json", "w") as f:
        json.dump(globals_data, f, indent=4)