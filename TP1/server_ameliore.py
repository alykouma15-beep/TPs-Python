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
    while True:
        sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('127.0.01', port))
        listeduoclients=[]
        print('En ecoute sur {}'. format(sock. getsockname()))
        i=0
        while len(listeduoclients)<2:
            payload, duo = sock.recvfrom(MAX_BYTES)
            print(payload.decode('ascii'))
            listeduoclients.append(duo)
            if i==0:
                text="Tu as ete enregistree, en attente de lautre client"
                data=text.encode('ascii')
                sock.sendto(data,listeduoclients[0])
            else:
                text="Tunnel etablie, vous pouvez communiquez"
                data=text.encode('ascii')
                sock.sendto(data,listeduoclients[0])
                sock.sendto(data,listeduoclients[1])
            i=1
        for i in range(2):
            payload, duo = sock.recvfrom(MAX_BYTES)
            print(payload.decode('ascii'))
            paquetrenvoie=Paquet(payload,duo)
            for duo in listeduoclients:
                if paquetrenvoie.duo!=duo:
                    sock.sendto(paquetrenvoie.payload,duo)
                    break
    
if __name__== '__main__':
    server(1060)