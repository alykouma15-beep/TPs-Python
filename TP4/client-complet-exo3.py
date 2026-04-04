from os import wait
import socket
from _thread import *
import threading
import sys
import xml.etree.ElementTree as ET
import json
import datetime
import time

class Client:
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET,socket. SOCK_STREAM)
        self.menu=None
        self.envoie=None
        self.continuer=None
        self.bytes=""
    def connect(self,duo):
        self.s.connect(duo)
        
    def accept(self):
        return self.s.accept()

    def ecoute_des_messages(self):
        while True:
            chunk=self.s.recv(1024).decode('utf-8')
            if not chunk:
                break
            self.bytes+=chunk
            while "\n" in self.bytes:
                self.portion,self.bytes=self.bytes.split('\n',1)  
                self.notif=json.loads(self.portion)
                if self.notif["type"]=="ECRITURE":
                    print(f"Client {self.notif['clientID']} est entrain d'écrire...")#Interception des notifs de type ECRITURE
                    continue
                if self.notif["type"]=="MENU":
                    self.menu=self.notif
                    continue
                if self.notif["type"]=="CHOISISSEZ":
                    self.envoie=self.notif
                    continue
                if self.notif["type"]=="CONTINUER":
                    self.continuer=self.notif
                    continue
                if self.notif["type"]=="MESSAGE":
                    print("nouveau message recu:",self.notif["content"])
                if self.notif["type"] in ["ETAT","CONNEXION","DECONNEXION"]:
                    print(self.notif)
                if self.notif["type"]=="CHAT":
                    print(f"Client {self.notif['emetteur']} dit ->",self.notif['content'])
def main():
    host = '127.0.0.1'
    port = 12345
    client1=Client()
    client1.connect((host, port))
    message = f"""
    <client>
        <nom>Aly</nom>
        <date_connexion>{datetime.date.today()}</date_connexion>
        <lieu>Paris</lieu>
    </client>
    """
    client1.s.sendall(message.encode('utf-8'))#envoie du message d'identification en XML
    notif = json.loads(client1.s.recv(1024).decode('utf-8')) #Extraction JSON : reception de liste des autres clients connectés en json
    if notif["type"].startswith("informations sur"):
        connectes={}
        if len(notif)>=2:
            for k,v in notif.items():
                if k!="type":
                    connectes[k]=v
            print(f"les autres clients connectés sont : \n{connectes}") #affichage de la liste via parsing JSON
        else:
            print("Pas d'autres clients connectés pour le momment") #exception du cas où je suis le seul client
    notif=json.dumps({"type":"HELLO"})
    client1.s.sendall((notif+"\n").encode('utf-8')) #envoie de la notification de message initial HELLO
    start_new_thread(client1.ecoute_des_messages,())
    while True:
        while not client1.menu:
            time.sleep(0.1)#Attente du menu
        print(f"Clients dispo pour chatter: {client1.menu}") #Reception et affichage du menu
        client1.menu=None
        while not client1.envoie:
            time.sleep(0.1)#Attente de la demande d'envoie
        print(client1.envoie) #reception de la demande d'envoie de message
        client1.envoie=None
        target=int(sys.stdin.readline())
        notif=json.dumps({"type": "CHOIX", "clientID": target})
        client1.s.sendall((notif+"\n").encode('utf-8')) #envoie de la notif de choix au serveur
        print("choix envoyee au serveur")
        message=str(sys.stdin.readline()) #saisie du message
        client1.s.sendall(message.encode('utf-8'))
        print("message envoyee au serveur")
        while not client1.continuer:
            time.sleep(0.1)#Attente de la demande de continuer
        print(client1.continuer) #reception de la demande de continuer
        client1.continuer=None
        message=sys.stdin.readline().strip() #saisie de la volonté de continuer
        notif={"type": "CONTINUER", "choix": message}
        notifj=json.dumps({"type": "CONTINUER", "choix": message})
        client1.s.sendall((notifj+"\n").encode('utf-8'))
        print("saisie envoyé envoyee au serveur")
        notife=json.dumps({"type": "ETAT", "change": "OCCUPE", "addr": client1.s.getsockname()})
        client1.s.sendall((notife+"\n").encode('utf-8'))
        print(notife)
        if notif["choix"]=='n':
            print("deconnexion...")
            sys.exit() 
if __name__ =='__main__':
    main()