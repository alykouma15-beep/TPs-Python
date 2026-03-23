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
    sock = socket.socket(socket.AF_INET, socket. SOCK_DGRAM)
    text ='Le temps est {}'.format(datetime.now())
    payload = text.encode('ascii')
    paquetcli= Paquet(payload,('127.0.01', port))
    sock.sendto(paquetcli.payload,paquetcli.duo)
    print(' mon adresse est {}'.format(sock.getsockname()))
    payload, duo = sock.recvfrom(MAX_BYTES)
    paquetserv=Paquet(payload,duo)
    print(paquetserv.text)
    sock.sendto(paquetserv.payload, paquetserv.duo)
    print(f"mon IP extrait de mon instance paquet est {paquetserv.ip}")
if __name__=='__main__':
    client(1060)