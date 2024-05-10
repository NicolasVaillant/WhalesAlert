import json
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path
import websocket
import traceback
from decimal import Decimal

# Version pc
tweet_json = Path("resources", "config_python", "ethereum", "tweet.json")
config_json = Path("resources", "config_python", "ethereum", "config.json")
coins_json = Path("resources", "data_coins")
tx_data_json = Path("resources", "data_tx")

# Version serveur
# tweet_json = Path("/home", "container", "webroot","resources", "config_python", "ethereum", "tweet.json")
# config_json = Path("/home", "container", "webroot","resources", "config_python", "ethereum", "config.json")
# coins_json = Path("/home", "container", "webroot","resources", "data_coins")
# tx_data_json = Path("/home", "container", "webroot","resources", "data_tx")

logger_fonction_websocket_analyze = logging.getLogger('websockets')
if not logger_fonction_websocket_analyze.handlers:
    logger_fonction_websocket_analyze.setLevel(logging.INFO)
    filenamelog = Path("logs", "websocket.log")
    handler = TimedRotatingFileHandler(filenamelog, when='midnight', interval=1, backupCount=7, encoding='utf-8')
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger_fonction_websocket_analyze.addHandler(handler)

with open(tweet_json, "r") as f:
    globals_data = json.load(f)

last_transaction_value: float = 0.0
last_known_block_index = globals_data.get('last_known_block_index', 0)
tweets_this_day = globals_data.get('tweets_this_day', 0)
day = globals_data.get('day', datetime.datetime.now().day)
post = globals_data.get('post', 0)
price = globals_data.get('price', 0)

pending_transactions = {}
f.close()

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

def get_token_price(token_name, token_value):
    token_name = ''.join(c for c in token_name if c.isprintable()).strip()
    token_file_name = token_name.replace(' ', '_').lower() + '.json'
    folder_path = f"{coins_json}/{token_file_name}"
    if os.path.exists(folder_path):
        with open(folder_path, 'r') as f:
            data = json.load(f)
        token_volume = float(data.get('price_change_7D_percent', 0))
        token_supply = int(data.get('supply', 0))
        if token_volume > 0 :
            token_price = float(data.get('last_price_usd', 0))
            amount = token_price * float(round(token_value, 2))
            return amount, token_supply
        else :
            return None, None
    else :
        return None, None

def decode_erc20_data(data):
    method_hash = data[:10]
    if method_hash == '0xa9059cbb':
        to_address = '0x' + data[34:74]
        token_value = int(data[74:], 16)
        return {'to': to_address, 'value': token_value}
    return None

def safe_decode(data):
    encodings = ['utf-8', 'ascii', 'latin1']
    for encoding in encodings:
        try:
            decoded_text = data.decode(encoding).strip()
            if decoded_text.isprintable():
                return decoded_text
        except UnicodeDecodeError:
            pass
    return data.decode('utf-8', 'ignore').strip()

def save_tx(total_out, value, tx_percentage_of_supply, url_tx_hash, token_file):
    token_file = os.path.join(tx_data_json, token_file)
    directory = os.path.dirname(token_file)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    try:
        with open(token_file, 'r') as file:
            transactions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        transactions = []

    new_transaction = {
        'amount': total_out,
        'value': value,
        'porcentage_supply': tx_percentage_of_supply,
        'url': url_tx_hash,
        'date': datetime.datetime.now().isoformat()
    }

    transactions.insert(0, new_transaction)

    with open(token_file, 'w') as file:
        json.dump(transactions, file, indent=4)

def get_ethereum_price() -> float:
    with open(tweet_json, "r") as f:
        globals_data = json.load(f)
    f.close()
    return globals_data['price'], globals_data['supply']

def on_message(ws, message):
    data = json.loads(message)
    
    price, circulating_supply = get_ethereum_price()

    if 'method' in data and data['method'] == 'eth_subscription':
        params = data['params']

        if isinstance(data, dict):
            if 'subscription' in params and params['subscription']:
                result = params['result']
                block_hash = str(result['hash'])
                request_transactions = json.dumps({
                    "jsonrpc": "2.0",
                    "method": "eth_getBlockByHash",
                    "params": [block_hash, True],
                    "id": 1
                })
                ws.send(request_transactions)

    elif 'result' in data and data['result'] is not None and 'transactions' in data['result']:
        transactions = data['result']['transactions']
        for tx in transactions:
            if tx['input'].startswith('0xa9059cbb'):
                erc20_data = decode_erc20_data(tx['input'])
                if erc20_data is not None :
                    erc20_data["value"] = Decimal(erc20_data['value']) / Decimal('1e18')
                    if float(erc20_data["value"]) > 10000.0:
                        pending_transactions[tx['hash']] = erc20_data
                        request_token_name = json.dumps({
                                "jsonrpc": "2.0",
                                "method": "eth_call",
                                "params": [{
                                    "to": tx['to'],
                                    "data": "0x06fdde03"
                                }, "latest"],
                                "id": tx['hash']
                        })
                        ws.send(request_token_name)

            amount = float(int(tx['value'], 16)) / 10**18
            if amount > 10000.0: 
                tx_percentage_of_supply = (float(amount) / float(circulating_supply)) * 100
                url_tx_hash = f"https://etherscan.io/tx/{tx['hash']}"
                total_out_str = human_format(amount)
                token_file_name = "tx_ethereum.json"

                save_tx(total_out_str,round(float(price) * amount, 2) , round(tx_percentage_of_supply,4), url_tx_hash, token_file_name)

    elif 'result' in data and 'id' in data:
        result = data['result']
        if result is not None and len(result) > 2 :
            token_info = str(safe_decode(bytes.fromhex(result[2:]))).strip()
            if pending_transactions == {}:
                return
            tx_info = pending_transactions[data['id']]
            token_info = ''.join(c for c in token_info if c.isprintable()).strip()
            token_price, supply = get_token_price(token_info, tx_info['value'])
            if token_price is not None and supply is not None:
                if supply > 0 : 
                    tx_percentage_of_supply = (float(tx_info['value']) / float(supply)) * 100
                else : 
                    tx_percentage_of_supply = 0
                if token_price > 10000:
                    token_price = float(token_price)
                    total_out_str = human_format(token_price)
                    url_tx_hash = f"https://etherscan.io/tx/{data['id']}"

                    token_name = ''.join(c for c in token_info if c.isprintable()).strip()
                    token_file_name = 'tx_' + token_name.replace(' ', '_').lower() + '.json'
                    save_tx(total_out_str,round(float(token_price), 2) , round(tx_percentage_of_supply,4), url_tx_hash, token_file_name)
    else:
        return

def on_error(ws, error):
    logger_fonction_websocket_analyze.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"### Connexion fermée ### : {close_status_code} / {close_msg}")

def on_open(ws):
    print("Connection opened ETH")
    subscribe_request = json.dumps({
            "jsonrpc": "2.0",
            "method": "eth_subscribe",
            "params": ["newHeads"],
            "id": 1
        })
    ws.send(subscribe_request)

def start_listening():
    ws = websocket.WebSocketApp("wss://ethereum-rpc.publicnode.com",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()

def job_ethereum() -> None:
    logger_fonction_websocket_analyze.info("Job ethereum")
    start_listening()
