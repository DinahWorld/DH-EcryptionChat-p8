import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from dh import *

class DH_Interface:
    def __init__(self):
        self.nickname = "Anonyme"
        self.not_my_public_key = 0
        self.public_key = 0
        self.private_key = 0
        self.message = ""
        self.entry_empty = True
        self.completed = False
        self.encryption_mode = False
        self.p = 0
        self.g = 0
        self.secret_value = 0

        builder = Gtk.Builder()
        builder.add_from_file(
            "glade/client_interface.glade"
        )  
        # On recupere tout les objets du fichier glade
        window = builder.get_object("client_window")
        self.textview = builder.get_object("textView")
        self.btnsend = builder.get_object("btnSend")
        self.send_public_key = builder.get_object("send_public_key")
        self.entry = builder.get_object("entry")
        self.instruction_label = builder.get_object("instruction")
        self.instruction_label.set_text("Entrez votre pseudo 🤫")

        self.my_public_key = builder.get_object("my_public_key")
        self.public_key_entry = builder.get_object("public_key_entry")

        self.bf = self.textview.get_buffer()
        self.entry.connect("activate", self.send)
        self.btnsend.connect("clicked", self.send)

        self.send_public_key.connect("clicked", self.dh_receive_public_key)
        self.public_key_entry.connect("activate", self.dh_receive_public_key)

        window.connect("delete-event", Gtk.main_quit)
        # On affiche nos objects
        window.show_all()
        # On les affichera plus tard lorsque l'utilisateur aura 
        # entré son pseudo 
        self.send_public_key.hide()
        self.public_key_entry.hide()
        self.my_public_key.hide()

    # Fonction qui renvoie True si on a toutes les informations
    # nécessaire pour le lancement du tchat
    def information(self):
        if self.completed == True:
            return True
        else:
            return False
    
    # Fonction qui récupere ce que l'on inscrit dans notre entry
    def send(self, e):
        text = self.entry.get_text()
        # Si on a pas rentré toutes nos informations à propos
        # de la clé dh et le prénom on ne dira pas que l'utilisateur
        #souhaite envoyer un message
        if self.completed == False:
            self.instruction_label.set_text("Entrez votre message")
            self.nickname = text
            self.entry.set_text("")
            self.send_public_key.show()
            self.public_key_entry.show()
            self.my_public_key.show()
            self.completed = True
        else:
            self.entry_empty = False
            self.message = text
            self.entry.set_text("")
 
    # Fonction qui entrer dans le textview le texte que l'on souhaite
    # inscrire 
    def enter_text(self, text):
        self.bf.insert_markup(self.bf.get_end_iter(),text + '\n',-1)
        self.textview.set_buffer(self.bf)

    # Un setteur 
    def set_e_p(self, p, g):
        self.p = p
        self.g = g
        
    # Fonction qui va initialiser nos variables pour préparer le chiffrement
    def dh_info(self,p,g):
            self.p = int(p)
            self.g = int(g)
            self.secret_value = secret_value_gen(self.p)
            self.public_key = dh_public_key(self.g,self.secret_value,self.p)
            self.my_public_key.set_text(str(self.public_key))

    # Fonction qui recupere la clé publique de l'utilisateur
    # On considere qu'une fois la clé reçu on lance le chiffrement en mettant la variable
    # encryption_mode sur True
    def dh_receive_public_key(self,e):
        self.not_my_public_key = int(self.public_key_entry.get_text())
        self.private_key = dh_private_key(self.not_my_public_key,self.secret_value,self.p)
        self.encryption_mode = True
        
    # Fonction qui récupere le message entré dans notre entry
    def get_message(self):        # Une fois notre message récupéré on indique que il n'y a aucun message
        self.entry_empty = True
        if self.encryption_mode == True:
                enc_m = dh_enc(self.message,self.private_key,self.p)
                return "- {}: {}".format(self.nickname,enc_m)
        else:
                return "- {}: {}".format(self.nickname, self.message)
    
    # Fonction qui entre dans le textview notre message
    def set_message(self,message):
        split_m = message.split(' ', 2)
        # Pour éviter de calculer à chaque fois le message
        # On ne chiffre uniquement lorsque le mode Chiffrement est activé
        # Et que c'est le message du locuteur et non de l'utilisateur
        if split_m[1] != self.nickname + ":" and self.encryption_mode == True:
            dec_m = dh_dec(int(split_m[2]),self.private_key,self.p)
            self.enter_text(f"{split_m[0]}{split_m[1]} {dec_m}")
        elif split_m[1] == (f"{self.nickname}:"):
            self.enter_text(f"{split_m[0]}{split_m[1]} {self.message}")            
        else:
            self.enter_text(message)

    def main(self):
        Gtk.main()
        return 0
