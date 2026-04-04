import socket
from _thread import *
import threading
import sys
import datetime
import xml.etree.ElementTree as ET
class Client:
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET,socket. SOCK_STREAM)
        self.nv="".encode('ascii')
        
    def connect(self,duo):
        self.s.connect(duo)
        
    def accept(self):
        return self.s.accept()

    def ecoute_des_messages(self):
        while True:
            self.nv=self.s.recv(1024)
            print(f"nouveau message reçu : {self.nv.decode('ascii')}")
def main():
    host = '127.0.0.1'
    port = 12345
    client1=Client()
    client1.connect((host, port))
    message = """
    <client>
        <nom>client1</nom>
        <date_connexion>19/04/2021</date_connexion>
        <lieu>Paris</lieu>
    </client>
    """ #Création du message XML
    client1.s.send(message.encode('ascii'))#Envoie du message XML
    """data = client1.s.recv(1024)
    print('message recu du serveur : ', data.decode('ascii') )#reception de liste des autres clients connectés
    client1.s.send("hello".encode('ascii')) #envoie du premier data1 dans communication_client 
    start_new_thread(client1.ecoute_des_messages,())
    while True:
        data = client1.nv #reception du menu de choix
        print(data.decode('ascii'))
        target=str(int(sys.stdin.readline()))
        client1.s.send(target.encode('ascii'))
        print("choix envoyee au serveur")
        data = client1.nv #reception de la demande d'envoie de message
        print(data.decode('ascii'))
        message=str(sys.stdin.readline()) #saisie du message
        client1.s.send(message.encode('ascii'))
        print("message envoyee au serveur")
        data = client1.nv #reception de la demande de continuer
        print(data.decode('ascii'))
        message=str(sys.stdin.readline()) #saisie de la volonté de continuer
        client1.s.send(message.encode('ascii'))
        print("saisie envoyé envoyee au serveur")"""
if __name__ =='__main__':
    main()