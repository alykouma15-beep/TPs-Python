import socket
MAX_BYTES = 65535

class Paquet:
    def __init__(self,payload,duo) -> None:
        self.payload=payload
        self.duo=duo
        self.ip=duo[0]
        self.port=duo[1]
        self.text=payload.decode('ascii')
    def actualiser_payload(self):
        self.payload=self.text.encode('ascii')
    def actualiser_text(self):
        self.text=self.payload.decode('ascii')
def server (port):
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.01', port))
    print('En ecoute sur {}'. format(sock. getsockname()))
    while True:
        payload, duo = sock.recvfrom(MAX_BYTES)
        paquetclient=Paquet(payload,duo)
        print(f"Le client {paquetclient.duo} dit {paquetclient.text}")
        paquetrenvoie=paquetclient
        paquetrenvoie.text=f"les donnees sont de taille {len(paquetrenvoie.payload)}"
        paquetrenvoie.actualiser_payload()
        sock.sendto(paquetrenvoie.payload,paquetrenvoie.duo)
    
if __name__== '__main__':
    server(1060)