from encodings.punycode import T
import socket
import argparse
import sys

HOST = '127.0.0.1'
PORT = 1060

class Server:
    def __init__(self,host,port) -> None:
        self.s = socket.socket(socket.AF_INET,socket. SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket. SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.host=host
        self.port=port
        self.duo = f"({self.host},{self.port})"
        
    def listen(self):
        self.s.listen(1)
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
        return data.decode('ascii')


class Client:
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET,socket. SOCK_STREAM)
        
    def connect(self,duo):
        self.s.connect(duo)
        
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
        return data.decode('ascii')

def server():
    server1=Server(HOST,PORT)
    server1.listen()
    while True:
        print('le serveur ecoute a cette adresse ', server1.duo)
        sc, sockname = server1.accept()
        print(' le serveur a accepte une connection de ', sockname)
        print('Une connexion : ', sc.getsockname(), ' et ', sc.getpeername ())
        taille = server1.ecoute(sc, 2)
        taille=int(taille)
        print(f"parfait message de taille {taille} attendue")
        message = server1.ecoute(sc, taille)
        print(f'les {taille} octets recu : ', repr(message))
        print("je suis le serveur: ecris le message")
        data=sys.stdin.readline()
        taille=str(len(data))
        taille=taille.encode('ascii')
        sc.sendall(taille)
        print("message ecrit")
        data=data.encode('ascii')
        sc.sendall(data)
        sc.close ()
        print("Une reponse a ete envoye, la socket est fermee")

    
def client():
    client1=Client()
    client1.connect((HOST, PORT))
    print('le serveur a assigne {} comme socket pour le client'. format(client1.s.getsockname()))
    print("je suis le client: ecris le message")
    data=sys.stdin.readline()
    taille=str(len(data))
    taille=taille.encode('ascii')
    client1.s.sendall(taille)
    print("message ecrit")
    data=data.encode('ascii')
    client1.s.sendall(data)
    tailleserv=client1.ecoute(client1.s,2)
    tailleserv=int(tailleserv)
    print(f"Je suis le client, OK : message de taille {tailleserv} attendu")
    reply= client1.ecoute(client1.s, tailleserv)
    print('le serveur a repondu : ', repr(reply))
    client1.s.close()
  
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Donner client ou serveur")
    parser.add_argument("type")
    args=parser.parse_args()
    if args.type=="server":
        server()
    else:
        client()