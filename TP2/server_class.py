import socket

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
        return data


def server():
    server1=Server(HOST,PORT)
    server1.listen()
    while True:
        print('le serveur ecoute a cette adresse ', server1.duo)
        sc, sockname = server1.accept()
        print(' le serveur a accepte une connection de ', sockname)
        print('Une connexion : ', sc.getsockname(), ' et ', sc.getpeername ())
        message = server1.ecoute(sc, 9)
        print('les 16 octets recu : ', repr(message))
        data=' Au revoir !'
        data=data.encode('ascii')
        sc.sendall(data)
        sc.close ()
        print("Une reponse a ete envoye, la socket est fermee")
        
if __name__ == '__main__':
    server ()