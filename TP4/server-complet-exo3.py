import socket
from _thread import *
import threading
import sys
import xml.etree.ElementTree as ET
import json

print_lock = threading.Lock()

class Clientsock:
    def __init__(self,c,addr) -> None:
        self.c=c
        self.addr=addr
        self.count=0
class Server:
    def __init__(self,host,port) -> None:
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.host=host
        self.port=port
        self.duo = f"({self.host},{self.port})"
        self.registry={}
        self.listec=[]
        self.i=0
        self.count=0
        
    def listen(self,n):
        self.s.listen(n)
    def accept(self):
        return self.s.accept()

    def ecoute(self,sock, length):
        data = ''
        data=data.encode('utf-8')
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('la socket a ete fermee')
            data += more
        return data
    
    def communication_client (self,c,id):
        while True:
            try:
                notif = json.loads(c.recv(1024).decode('utf-8'))#Notification de connexion recu du client
                if notif["type"] !="HELLO":
                    print( 'Bye')
                    for k,v in self.registry.items():
                        if v[0]!=c:
                            notif=json.dumps({"type": "DECONNEXION","clientID": id })#Notification aux autres de la nouvelle connexion
                            v[0].sendall((notif+"\n").encode('utf-8'))
                    break
                data = json.dumps({"type": "MESSAGE", "content": 'Welcome'})
                c.sendall ((data+"\n").encode('utf-8')) #envoie du welcome
                for k,v in self.registry.items():
                    if v[0]!=c:
                        notif=json.dumps({"type": "CONNEXION","clientID": id })#Notification aux autres de la nouvelle connexion
                        v[0].sendall((notif+"\n").encode('utf-8'))
                break
            except BrokenPipeError:
                print( 'Bye')
                for k,v in self.registry.items():
                    if v[0]!=c:
                        notif=json.dumps({"type": "CONNEXION","clientID": id })#Notification aux autres de la nouvelle connexion
                        v[0].sendall((notif+"\n").encode('utf-8'))
                        break
                if f"clientid{id}" in self.registry:
                    print_lock.acquire()
                    self.count-=1
                    self.registry.pop(f"clientid{id}") #suppression du client actif du self.registry pour actualisation
                    print_lock.release()
        print_lock.acquire()
        self.count+=1
        print_lock.release()
        if self.count<2:
            print("Le serveur attend minimum 2 clients")
        while True:
            if self.count>=2:#attente de minimum 2 clients
                break
        # Menu de choix de client
        while True:
            try:   
                notif={k:v[1] for k,v in self.registry.items() if v[2]!=id}#Le serveur envoie le menu des autres clients dispo
                notif['type']="MENU" #Creation de la notification de menu
                notif=json.dumps(notif) #passage en JSON
                c.sendall((notif+"\n").encode('utf-8'))#Envoie du MENU en JSON
                print(f"envoie du menu au client {id}")
                notif=json.dumps({"type":"CHOISISSEZ","content": "choisissez le client avec qui vous voulez communiquez en tapant un id exemple 1,2,etc"})
                c.sendall((notif+"\n").encode('utf-8')) #demande du destinataire de son message
                notif=json.loads(c.recv(1024).decode('utf-8'))#Reception de la notif du choix du destinataire
                print(notif)
                target=notif['clientID']
                for k,v in self.registry.items():
                    if v[2]==target:
                        notif=json.dumps({"type": "ECRITURE","clientID": id })#Notification aux autres de la nouvelle connexion
                        v[0].sendall((notif+"\n").encode('utf-8'))
                        break
                c.sendall((json.dumps({"type": "MESSAGE", "content": "parfait ecrivez votre message"})+"\n").encode('utf-8'))
                message=c.recv(1024).decode('utf-8')
                notif=json.dumps({"type":"CHAT","emetteur": id,"content":f"{message}"})
                if f"clientid{target}" in self.registry:
                    self.registry[f"clientid{target}"][0].sendall((notif+"\n").encode('utf-8'))
                    c.sendall((json.dumps({"type": "CONTINUER", "content": "distribuee ! voulez vous rester?y/n"})+"\n").encode('utf-8'))
                    continuer=c.recv(1024)
                    continuer=json.loads(continuer.decode('utf-8'))
                    print(continuer)
                    notif=json.loads(c.recv(1024).decode('utf-8'))
                    if notif["type"]=="ETAT":#Interception des notifications de type ETAT
                        for k,v in self.registry.items(): #recuperation d'abord de l'ID du client dans le registre
                            if v[1][1]==notif["addr"][1]:
                                idcli=v[2]
                                change=notif['change']
                                print(notif)
                                break
                        for k,v in self.registry.items():
                            notif=json.dumps({"type": "ETAT","clientID": idcli,"change": change })#Notification aux autres du nouvel etat
                            v[0].sendall((notif+"\n").encode('utf-8'))
                    if continuer["choix"]=='n':
                        break
                else:
                    c.sendall((json.dumps({"type":"MESSAGE","content":"client inexistant"})+"\n").encode('utf-8'))
            except json.JSONDecodeError:
                break
            except BrokenPipeError:
                for el in self.listec:
                    message=json.dumps({"type":"MESSAGE","content":f"Le client {id} libere"}) + "\n"
                    print(message)
                    el.sendall(message.encode('utf-8'))
                    break
        c.close()
        if f"clientid{id}" in self.registry:
            print_lock.acquire()
            self.count= (self.count-1 if self.count>0 else 0)
            self.registry.pop(f"clientid{id}") #suppression du client actif du self.registry pour actualisation
            print_lock.release()
            for k,v in self.registry.items():
                if v[0]!=c:
                    notif=json.dumps({"type": "DECONNEXION","clientID": id })#Notification aux autres de la nouvelle connexion
                    v[0].sendall((notif+"\n").encode('utf-8'))
            print(notif)
   
   
    def ecoute_des_messages(self):
        while True:
            self.bytes=self.s.recv(1024)
            try:
                self.notif=json.loads(self.bytes.decode('utf-8').strip())
                if self.notif["type"]=="ETAT":#Interception des notifications de type ETAT
                    for k,v in self.registry.items(): #recuperation d'abord de l'ID du client dans le registre
                        if v[1]==self.notif["addr"]:
                            idcli=v[2]
                            change=self.notif['change']
                            break
                    for k,v in self.registry.items():
                        notif=json.dumps({"type": "ETAT","clientID": idcli,"change": change })#Notification aux autres du nouvel etat
                        v[0].sendall((notif+"\n").encode('utf-8'))
                    continue
            except json.JSONDecodeError:
                print(f"nouveau message reçu : {self.bytes.decode('utf-8')}")
                continue
            print(f"nouveau message reçu : {self.bytes.decode('utf-8')}")
              
        
    
def thread_ecoute():
    host = '127.0.0.1'
    port = 12345
    server1=Server(host,port)
    print ("socket bindee au port ",port)
    server1.listen(5)
    print ("le serveur est en ecoute...")
    while True:
        c,addr = server1.accept()
        server1.listec.append(c)
        server1.i+=1
        print(f"nouvelle id {server1.i}")
        root=ET.fromstring(c.recv(1024).decode('utf-8'))
        print(f"connecté au client {root[0].text} le {root[1].text} à {root[2].text}")#Reception du message d'identification en XML
        notif={"type":"informations sur le nombre de clients connectés"}
        double=server1.registry
        for k,v in double.items():
            notif[k]=v[1]
        notif=json.dumps(notif)
        c.sendall((notif+"\n").encode('utf-8')) #envoie des autres clients connectés en JSON
        client1sock=Clientsock(c,addr)
        kid=f"clientid{server1.i}"
        server1.registry[kid]=[client1sock.c,client1sock.addr,server1.i]
        print('Connecte au client : ', addr[0], ':', addr[1])
        print_lock.acquire()
        for cf,el in enumerate(server1.listec):
            if addr == el.getpeername():
                del server1.listec[cf]
        print_lock.release()
        start_new_thread(server1.communication_client, (c,server1.i))
if __name__ =='__main__':
    thread_ecoute()