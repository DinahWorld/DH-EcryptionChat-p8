import socket
import threading
from dh import *
from dh_interface import *

# On lance le thread qui va lancer l'interface graphique
user = DH_Interface()
gui_thread = threading.Thread(target=user.main)
gui_thread.start()

user.enter_text("Bienvenue sur le chat DF Encryption")
user.enter_text("Veuillez vous envoyez vos clé respective")
user.enter_text("Entrez votre pseudo")

# Tant que l'utilisateur n'aura pas fourni son pseudo
# On ne continue pas le programme
while True:
    if user.information() == True:
        break

"""
    On se connecte au server
    Le client a besoin de deux thread, un qui va recevoir constamment
    les données du serveur et le deuxieme qui va envoyer nos messages 

"""
""""""
# Connection To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5555))

"""
    Fonction qui va constamment recevoir les messages et les afficher sur l'écran
    Si on recoit le message 'NICK' on envoie notre pseudo
    sinon il y a une erreur alors on arrete la connexion avec le serveur
    et notre boucle
"""
# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(2048).decode("ascii")
            first_word = message.split(" ", 1)[0]
            
            # Lorsque le message reçu commence par NICK alors cela voudra dire
            # que le serveur nous demande le prénom de l'utilisateur et nous donne p g
            if first_word == "NICK":
                # On reçoit alors les valeurs p et g
                split_m = message.split(" ", 2)
                user.dh_info(split_m[1],split_m[2])                
                client.send(user.nickname.encode("ascii"))
            # On considere que si le message commence par "-" alors on a un message
            elif first_word == '-':
                user.set_message(message) 
            else: 
                user.enter_text(message)
        except:
            # Close Connection When Error
            print("Une erreur !\n")
            client.close()
            break


"""
    La fonction write attendre que l'on envoie un message
"""
# Sending Messages to Server
def write():
    while True:
        # On enovi au serveur uniquement lorsque l'entry contiendra un texte
        if(user.entry_empty == False):
            message = user.get_message()
            client.send(message.encode("ascii"))


"""
    Deux threads qui vont lancer les deux fonctions
"""
# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
