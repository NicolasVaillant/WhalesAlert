import json
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path
import websocket
from os import name, system
import ssl
import certifi

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

if name == "nt":
    # Version pc
    search_bar = Path("resources", "data_scrap", "coins_list.json")
    data_coin = Path("resources", "data_coins")
else:
    # Version serveur
    search_bar = Path("/home", "container", "webroot","resources", "data_scrap", "coins_list.json")
    data_coin = Path("/home", "container", "webroot","resources", "data_coins")

logger_fonction_websocket = logging.getLogger('websockets')
if not logger_fonction_websocket.handlers:
    logger_fonction_websocket.setLevel(logging.INFO)
    filenamelog_websocket= Path("logs", "websocket.log")
    handler_websocket = TimedRotatingFileHandler(filenamelog_websocket, when='midnight', interval=1, backupCount=7, encoding='utf-8')
    handler_websocket.suffix = "%Y-%m-%d"  # suffixe le fichier de log avec la date du jour
    handler_websocket.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger_fonction_websocket.addHandler(handler_websocket)

# Fonction pour lire le fichier de correspondance entre symboles et noms.
def read_comparison_table(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)
    
# Fonction de traitement et de mise à jour des données reçues.
def process_and_update_data(received_data, comparison_table):
    for key in received_data['data']:
        symbol = key.split("/")[1]  # Extrait le symbole de la clé
        for coin in comparison_table:
            if coin['symbol'] == symbol:
                file_name = f"{data_coin}/{str(coin['name']).lower().replace(' ', '_')}.json"
                if os.path.exists(file_name) :
                    with open(file_name, 'r') as file:
                        target_data = json.load(file)

                    target_data['last_price_usd'] = received_data['data'][key]['value']
                    if received_data['data'][key]['supply'] != "null":
                        target_data['supply'] = float(received_data['data'][key]['supply'])

                    target_data['price_change_1H_percent'] = str(received_data['data'][key]['price_change_1H_percent'])
                    target_data['price_change_1D_percent'] = str(received_data['data'][key]['price_change_1D_percent'])
                    target_data['price_change_7D_percent'] = str(received_data['data'][key]['price_change_7D_percent'])
                    target_data['price_change_30D_percent'] = str(received_data['data'][key]['price_change_30D_percent'])
                    target_data['price_change_90D_percent'] = str(received_data['data'][key]['price_change_90D_percent'])
                    target_data['price_change_180D_percent'] = str(received_data['data'][key]['price_change_180D_percent'])
                    target_data['price_change_365D_percent'] = str(received_data['data'][key]['price_change_365D_percent'])
                    target_data['price_change_3Y_percent'] = str(received_data['data'][key]['price_change_3Y_percent'])
                    target_data['price_change_5Y_percent'] = str(received_data['data'][key]['price_change_5Y_percent'])
                    target_data['price_change_ALL_percent'] = received_data['data'][key]['price_change_ALL_percent']
                    target_data['price_change_YTD_percent'] = str(received_data['data'][key]['price_change_YTD_percent'])
                    if target_data['symbol'] == symbol :
                        with open(file_name, 'w') as file:
                            json.dump(target_data, file, indent=4)

                    break

def on_message(ws, message):
    try:
        # Parse le message JSON reçu.
        data = json.loads(message)

        # Lit la table de comparaison.
        comparison_table = read_comparison_table(search_bar)

        # Traite et met à jour les données avec la table de comparaison.
        process_and_update_data(data, comparison_table)

    except json.JSONDecodeError as e:
        print("Erreur de décodage JSON :", e)

def on_error(ws, error):
    logger_fonction_websocket.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    logger_fonction_websocket.info(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")   

def on_open(ws):
    print("Connection opened COINCODEX")
    ws.send(json.dumps({'action': 'refresh', 'what': 'all_coins_ticker'}))
    ws.send(json.dumps({'action': 'subscribe', 'data_format': 'binary'}))
    # print(f"Souscription envoyée: {subscribe_message}")

def start_listening():
    ws_app = websocket.WebSocketApp("wss://ws2.coincodex.com/subscriptions?transport=websocket&compression=false",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close
                                    )
    ws_app.run_forever(reconnect=10, sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False, "ssl_context": ssl_context})

def job_data_rtc():
    logger_fonction_websocket.info("Job websocket coincodex")

    start_listening()