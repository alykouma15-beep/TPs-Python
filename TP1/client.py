import socket
from datetime import datetime
MAX_BYTES = 65535

def client(port):
    sock = socket.socket(socket.AF_INET, socket. SOCK_DGRAM)
    text ='Le temps est {}'.format(datetime.now())
    data = text.encode('ascii')
    sock.sendto(data, ('127.0.01', port))
    print(' mon adresse est {}'.format(sock.getsockname()))
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('ascii')
    print(text)
    sock.sendto(data, address)
if __name__=='__main__':
    client(1060)