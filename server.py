import socket
import threading
from rsa import *

#Connection Data
host = '127.0.0.1'
port = 5555

# Starting Server
'''Lorsque l'on défini un socket on doit passer deux parametre
    Ils définissent le type de socket que l'on veut

    1er parametre : AF_INET indique que nous utilisont un socket internet
    plutot qu'un socket unix

    2e parametre : le protocol que nous voulons, SOCK_STREAM indique
    que nous utilisons TCP et pas UDP

    Ensuite nous lions notre hote et notre port en les passant dans tuple
    qui contient les deux valeurs puis nous passons le serveur on mode écoute
'''
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((host,port))
server.listen()

'''
    Les deux listes serviront à garder les clients connecté et leurs pseudo
'''
# List For Clients and their Nicknames
clients = []
nicknames = []
'''
    La fonction va nous servir à diffuser les messages
    Il va envoyer le message a chaque client 
'''

# Sending Messages to All Conected
def broadcast(message):
    for client in clients:
        client.send(message)

'''
    A chaque fois qu'un client sera connecté on lance la fonction
    Il recoit le message du client et le diffuse a tout les clients
    S'il y a un probleme avec la connexion du client on enleve sonpseudo
    ,on éteint la connexion et on diffuse que le client a quitté le tchat
    apres on arrete la boucle et cette discussion arrivera a terme
'''
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(2048)
            print(message)
            broadcast(message)
        except:
            # Removing and Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break;
'''
    Lorsque l'on sera pret pour lancer le serveur nous executerons la fonction receive
    Il accepte les nouvelles connections des utilisateurs. Une fois un client
    connecté il envoie le string Nick qui dira au client que le pseudo est requis, ensuite
    nous attondons une réponse qui contiendra le pseudo and on ajoutera le client avec le pseudo
    dans notre liste. Apres cela on affiche and diffuse l'information
    A la fin on lance un nouveau thread qui lancera la fonction handle pour le client
    On doit toujours chiffré le message que l'on va envoyer pour ensuite le décoder
'''

def receive():
    while True:
            #Accept Connection
            client, address = server.accept()
            print("Connected with {}".format(str(address)))
            
            # Request And Store Nickname
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(2048).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)
            
                 
            # Print And Broadcast Nickname
            print("Nickname is {}".format(nickname))
            broadcast("{} joined!".format(nickname).encode('ascii'))
            client.send(('Connected to server!\n').encode('ascii'))

            # Start Handling Thread For Client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()


receive()