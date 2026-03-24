import socket

HOST= '127.0.0.1'
PORT = 1060
def recv_all(sock, length):
    data= ''
    data=data.encode('ascii')
    while len(data)< length:
        more = sock.recv(length - len (data))
        if not more:
            raise EOFError('la socket a ete fermee')
        data += more
        
    return data
    
def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print('le serveur a assigne {} comme socket pour le client'. format(s. getsockname()))
    data='Bonjour !'
    data=data.encode('ascii')
    s.sendall(data)
    reply= recv_all(s, 11)
    print('le serveur a repondu : ', repr(reply))
    s.close()
    
if __name__=='__main__':
    client()