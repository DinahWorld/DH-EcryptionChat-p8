import socket 
import threading
from rsa import *
from interface import *

user = UserInterface();

gui_thread = threading.Thread(target=user.main)
gui_thread.start()


user.enter_text('Génération des clé en cours... 🔑')
key = gen_rsa_key(2048)

user.set_user_key(key)
user.enter_text('Entrez votre pseudo et la clé publique de votre interlocuteur')
print("my key",user.my_private_key)

# Choosing Nickname
while True:
    if user.information() == True:
        break
print("not my key",user.not_my_key)

'''
    On se connecte au server
    Le client a besoin de deux thread, un qui va recevoir constamment
    les données du serveur et le deuxieme qui va envoyer nos messages 

'''
''''''
#Connection To Server
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',5555))

'''
    Fonction qui va constamment recevoir les messages et les afficher sur l'écran
    Si on recoit le message 'NICK' on envoie notre pseudo
    sinon il y a une erreur alors on arrete la connexion avec le serveur
    et notre boucle
'''
# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(2048).decode('ascii')
            first_word = message.split(' ', 1)[0]            
            if message == 'NICK':
                client.send(user.nickname.encode('ascii'))
            elif first_word == '-':
                split_m = message.split(' ', 2)
                if split_m[1] != user.nickname+':':
                    
                    dec_m = rsa_dec(int(split_m[2]),user.my_private_key)
                    user.enter_text(split_m[0] + split_m[1] + " " + str(dec_m))
                else:
                    user.enter_text(split_m[0] + split_m[1] + " " + user.message)
            else: 
                user.enter_text(message)
        except:
            # Close Connection When Error
            print("Une erreur !\n, Avez vous bien renseigné une bonne clé ?")
            client.close()
            break

'''
    La fonction v attendre que l'on envoie un message
'''
# Sending Messages to Server
def write():
    while True:
        #On chiffre uniquement lorsqu'on a un texte
        if user.entry_empty != True:
            print("sa")
            enc_m = rsa_enc(user.message,user.not_my_key)
            message = '- {}: {}'.format(user.nickname, enc_m)
            client.send(message.encode('ascii'))
            #Une fois notre message récupéré on indique que il n'y a aucun message
            user.entry_empty = True
'''
    Deux threads qui vont lancer les deux fonctions
'''
# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
