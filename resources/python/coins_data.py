import requests
import os
import json

# Définir le chemin de base pour l'enregistrement des informations des coins
chemin_base = 'D:\\Crypto\\Bot\\WhalesAlert\\resources\\data_coins'

# S'assurer que le chemin de base existe
if not os.path.exists(chemin_base):
    os.makedirs(chemin_base)

def sauvegarder_infos_coins():
    # Récupérer la liste des tickers (coins) depuis l'API Coinpaprika
    url_tickers = 'https://api.coinpaprika.com/v1/tickers/'
    response = requests.get(url_tickers)
    
    if response.status_code == 200:
        tickers = response.json()
        
        # Parcourir chaque ticker et sauvegarder ses informations dans un fichier JSON dédié
        for ticker in tickers[:20]:  # Limiter le nombre pour cet exemple
            nom_coin = ticker['name'].replace(' ', '_').lower()  # Utiliser le nom du coin, en minuscules et avec des underscores
            
            # Définir le chemin complet du fichier JSON pour le coin
            chemin_fichier = os.path.join(chemin_base, f'{nom_coin}.json')
            
            # Préparer les données à sauvegarder dans le format spécifié
            data_to_save = [ticker]
            
            # Sauvegarder les informations du coin dans un fichier JSON
            with open(chemin_fichier, 'w') as fichier:
                json.dump(data_to_save, fichier, indent=4)
            
            print(f'Informations sauvegardées pour : {nom_coin}')
    else:
        print('Erreur lors de la récupération des informations des coins depuis Coinpaprika')
