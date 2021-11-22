#!/usr/bin/env python3
# coding: utf-8
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

class UserInterface:
        def __init__(self):
                self.nickname = "Anonyme"
                self.not_my_key = [0,1]
                self.my_key = [0,1]
                self.message = ""
                self.entry_empty = True
                self.nickname_step = False
                self.key_e_step = False 
                self.key_n_step = False 
                self.completed = False
                
                builder = Gtk.Builder()
                builder.add_from_file('glade/client_interface.glade')  # Rentrez évidemment votre fichier, pas le miens!

                window = builder.get_object('client_window')
                self.textview = builder.get_object('textView')
                self.btnsend = builder.get_object('btnSend')
                self.entry = builder.get_object('entry')
                self.instruction_label = builder.get_object('instruction')
                self.instruction_label.set_text("Entrez votre pseudo 🤫")

                self.cle_publique = builder.get_object('cle_publique')
                self.cle_privee = builder.get_object('cle_privee')

                self.bf = self.textview.get_buffer()
                self.entry.connect('activate',self.send)
                self.btnsend.connect('clicked',self.send)
                        
                # Peut se faire dans Glade mais je préfère le faire ici, à vous de voir
                window.connect('delete-event', Gtk.main_quit)
                window.show_all()
                        
        def send(self,e):
                text = self.entry.get_text()
                if(self.completed == False):
                        if (self.nickname_step == False):
                                self.instruction_label.set_text("👉 Entrez la clé publique de votre interlocuteur e: 🤫")
                                self.nickname = text
                                self.nickname_step = True
                                self.entry.set_text("")
                        elif (self.key_e_step == False):
                                self.instruction_label.set_text("👉 Entrez la clé publique de votre interlocuteur n: 🤫")
                                self.not_my_key[0] = int(text);
                                self.key_e_step = True
                                self.entry.set_text("")
                        elif (self.key_n_step == False):    
                                self.instruction_label.set_text("Entrez votre message")
                                self.not_my_key[1] = int(text);
                                self.completed = True
                                self.key_n_step = True
                                self.entry.set_text("")
                        else : 
                                print(text)
                else :
                        text = self.entry.get_text()
                        self.entry_empty = False
                        self.message = text 
                        self.entry.set_text("")
        
        def enter_text(self,text):
                self.bf.insert_markup(self.bf.get_end_iter(),text + '\n',-1)
                self.textview.set_buffer(self.bf)

        def information(self):
                if(self.completed == True):
                        return True
                else:
                        return False
        
        def set_user_key(self,key):
                self.my_key = key
                self.cle_publique.set_text(str(key[0]))
                self.cle_privee.set_text(str(key[1]))   
        
        def main(self):
                Gtk.main()
                return 0





