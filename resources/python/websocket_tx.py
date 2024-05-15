import asyncio
import websockets
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from time import time
from collections import defaultdict
import os

# Définition du gestionnaire d'événements pour les modifications de fichiers
class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.debounce_period = 2  # Temps en secondes pour ignorer les modifications répétitives
        self.last_modified_times = defaultdict(lambda: 0)
        self.last_known_transaction = None  # Stocke la dernière transaction connue

    def on_modified(self, event):
        if not event.is_directory:  # Ignorer les dossiers
            current_time = time()
            # Vérifier si l'événement est suffisamment récent pour être envoyé
            if current_time - self.last_modified_times[event.src_path] > self.debounce_period:
                self.last_modified_times[event.src_path] = current_time
                asyncio.run(self.callback(event.src_path, event.event_type))

# Fonction callback appelée lorsque le fichier est modifié
async def notify_change(websocket, file_path, event_type):
    # Initialisation des variables pour la stratégie de réessai
    try_count = 0
    max_retries = 3
    wait_seconds = 1
    transactions = None

    # Boucle de réessai pour lire le fichier JSON
    while try_count < max_retries:
        try:
            with open(file_path, 'r') as file:
                transactions = json.load(file)
            # Si la lecture est réussie, sortez de la boucle de réessai
            break
        except json.JSONDecodeError as e:
            # Attendez un peu avant de réessayer si une erreur JSON est rencontrée
            print(f"Erreur de lecture du fichier JSON ({e}), tentative {try_count + 1}...")
            await asyncio.sleep(wait_seconds)
            try_count += 1

    # Après avoir sorti de la boucle de réessai, vérifiez si les transactions ont été lues avec succès
    if transactions is not None:
        # S'il y a des transactions et qu'elles sont différentes de la dernière connue
        if not handler.last_known_transaction or transactions[0] != handler.last_known_transaction:
            new_transactions = []
            for transaction in transactions:
                if transaction == handler.last_known_transaction:
                    break
                new_transactions.append(transaction)
            # Si de nouvelles transactions ont été trouvées, mettez à jour la dernière connue et envoyez-les
            if new_transactions:
                handler.last_known_transaction = new_transactions[0]
                message = json.dumps({'type': 'new_transactions', 'transactions': new_transactions})
                await websocket.send(message)
    else:
        # Si la lecture du fichier a échoué après toutes les tentatives, log ou gérez l'erreur ici
        print(f"Impossible de lire le fichier {file_path} après {max_retries} tentatives.")

# Fonction pour gérer le serveur WebSocket
async def file_change_server(websocket, path):
    global handler
    handler = FileChangeHandler(lambda path, event_type: notify_change(websocket, path, event_type))
    observer = Observer()
    observer.schedule(handler, path='resources/data_tx', recursive=True)
    observer.start()
    try:
        # Attendre que la connexion WebSocket soit fermée
        await websocket.wait_closed()
    finally:
        observer.stop()
        observer.join()

# Démarrer le serveur WebSocket
start_server = websockets.serve(file_change_server, "192.168.1.73", 6789)

# Exécuter le serveur WebSocket indéfiniment
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
