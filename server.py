import socket
MAX_BYTES = 65535

def server (port):
    sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.01', port))
    print('En ecoute sur {}'. format(sock. getsockname()))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print('Le client {} dit {!r}'.format(address, text))
        text='les donnees ont une taille de {} octets'.format(len(data))
        data = text.encode('ascii')
        sock.sendto(data, address)
    
if __name__== '__main__':
    server(1060)