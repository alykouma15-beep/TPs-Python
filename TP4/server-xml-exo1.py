import socket
from _thread import *
import threading
import sys
import xml.etree.ElementTree as ET

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
        data=data.encode('ascii')
        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('la socket a ete fermee')
            data += more
        return data
    
    def communication_client (self,c,id):
        while True:
            # data1 received from client
            data = c.recv(1024)
            if not data:
                print( 'Bye')
                for el in self.listec:
                    message=f"Le client id: {id} libere"
                    el.send(message.encode('ascii'))
                print_lock.release()
                break
            data = 'Welcome'
            c.send (data.encode('ascii')) #envoie du welcome
            print_lock.release()
            break
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
            autres={k:v[1] for k,v in self.registry.items() if v[2]!=id}#J'affiche le menu des autres clients dispo
            menu=f"{autres}"
            c.send(menu.encode('ascii'))
            c.send("choisissez le client avec qui vous voulez communiquez en tapant son id".encode('ascii'))
            target=c.recv(1024)
            target=int(str(target.decode('ascii')))
            c.send("parfait ecrivez votre message".encode('ascii'))
            message=c.recv(1024)
            if f"clientid{target}" in self.registry:
                self.registry[f"clientid{target}"][0].send(message)
                c.send("distribuee ! voulez vous rester?y/n".encode('ascii'))
                continuer=c.recv(1024)
                continuer=str(continuer.decode('ascii'))
                print(continuer)
                if continuer=='n':
                    break
            else:
                c.send("client inexistant".encode('ascii'))
        for el in self.listec:
            message=f"Le client {id} libere"
            el.send(message.encode('ascii'))
        c.close()
        if f"clientid{id}" in self.registry:
            self.count-=1
            self.registry.pop(f"clientid{id}") #suppression du client actif du self.registry pour actualisation
        
        
    
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
        print(recu:=c.recv(1024).decode('ascii'))#Reception du message XML
        root=ET.fromstring(recu)#objet racine
        print(root.tag) #nom de l'objet racine
        print(len(root)) #nombre d'enfants de la racine
        print(root[0].tag) #nom du premier enfant
        print(root[0].text)#contenu du premier enfant
        print(root[1].tag)# nom du deuxième enfant
        print(root[1].text)#contenu du deuxième enfant
        """string="liste actuelle d'autres clients connectees:\n"
        double=server1.registry
        for k,v in double.items():
            string+=f"{k}:{v[1]}\n"
        c.send(string.encode('ascii')) #envoie des autres clients connectés
        client1sock=Clientsock(c,addr)
        kid=f"clientid{server1.i}"
        server1.registry[kid]=[client1sock.c,client1sock.addr,server1.i]
        print(f"clients ajoutés : {server1.registry.keys()}")
        print_lock.acquire()
        print('Connecte au client : ', addr[0], ':', addr[1])
        for cf,el in enumerate(server1.listec):
            if addr == el.getpeername():
                del server1.listec[cf]
        start_new_thread(server1.communication_client, (c,server1.i))"""
if __name__ =='__main__':
    thread_ecoute()