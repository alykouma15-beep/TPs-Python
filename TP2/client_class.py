import socket

HOST= '127.0.0.1'
PORT = 1060
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
        return data
    
def client():
    client1=Client()
    client1.connect((HOST, PORT))
    print('le serveur a assigne {} comme socket pour le client'. format(client1.s.getsockname()))
    data='Bonjour !'
    data=data.encode('ascii')
    client1.s.sendall(data)
    reply= client1.ecoute(client1.s, 11)
    print('le serveur a repondu : ', repr(reply))
    client1.s.close()
    
if __name__=='__main__':
    client()