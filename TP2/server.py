import socket

HOST = '127.0.0.1'
PORT = 1060


def recv_all(sock, length):
    data = ''
    data=data.encode('ascii')
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('la socket a ete fermee')
        data += more
    return data

def server():
    s = socket.socket(socket.AF_INET,
    socket. SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket. SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        print('le serveur ecoute a cette adresse ', s.getsockname())
        sc, sockname = s.accept()
        print(' le serveur a accepte une connection de ', sockname)
        print('Une connexion : ', sc.getsockname(), ' et ', sc.getpeername ())
        message = recv_all(sc, 9)
        print('les 16 octets recu : ', repr(message))
        data=' Au revoir !'
        data=data.encode('ascii')
        sc.sendall(data)
        sc.close ()
        print("Une reponse a ete envoye, la socket est fermee")
        
if __name__ == '__main__':
    server ()