import socket
from _thread import *
import threading
print_lock = threading.Lock()

class Server:
    def __init__(self,host,port) -> None:
        self.s = socket.socket(socket.AF_INET,socket. SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket. SO_REUSEADDR, 1)
        self.s.bind((host, port))
        self.host=host
        self.port=port
        self.duo = f"({self.host},{self.port})"
        
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
    
    def communication_client (self,c):
        while True:
            # data received from client
            data = c. recv(1024)
            if not data:
                print( 'Bye')
                print_lock. release()
                break
            data = 'Welcome'
            c.send (data. encode())
        # Fermer la connexion
        c.close()
    
def thread_ecoute():
    host = ""
    port = 12345
    server1=Server(host,port)
    print ("socket bindee au port ",port)
    server1.listen(5)
    print ("le serveur est en ecoute...")
    while True:
        c,addr = server1.accept()
        print_lock.acquire()
        print('Connecte au client : ', addr[0], ':', addr[1])
        start_new_thread(server1.communication_client, (c,))
        server1.s.close()
if __name__ =='__main__':
    thread_ecoute()