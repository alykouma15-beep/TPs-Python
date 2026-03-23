import socket
from datetime import datetime
MAX_BYTES = 65535

class Paquet:
    def __init__(self,payload,duo) -> None:
        self.payload=payload
        self.duo=duo
        self.ip=duo[0]
        self.port=duo[1]
        self.text=payload.decode('ascii')
    def actualiser(self):
        self.payload=self.text.encode('ascii')
        self.text=self.payload.decode('ascii')

def client(port):
    print("Terminal du client 1")
    sock = socket.socket(socket.AF_INET, socket. SOCK_DGRAM)
    text =' mon adresse est {}'.format(sock.getsockname())
    payload = text.encode('ascii')
    paquetannonce= Paquet(payload,('127.0.01', port))
    sock.sendto(paquetannonce.payload,paquetannonce.duo)
    payload, duo = sock.recvfrom(MAX_BYTES)
    print(payload.decode('ascii'))
    payload, duo = sock.recvfrom(MAX_BYTES)
    print(payload.decode('ascii'))
    text ='je suis le client 1 Le temps est {}'.format(datetime.now())
    payload = text.encode('ascii')
    paquetcli= Paquet(payload,('127.0.01', port))
    sock.sendto(paquetcli.payload,paquetcli.duo)
    payload, duo = sock.recvfrom(MAX_BYTES)
    paquetserv=Paquet(payload,duo)
    print(paquetserv.text)
if __name__=='__main__':
    client(1060)