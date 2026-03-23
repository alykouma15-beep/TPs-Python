from ast import main
from base64 import decode, encode
import socket
import http.client
url="""GET /maps/geo?q=207+N.+Defiance+St%2C+AnchboLd%2C+ОH
        &output=json&oe=utf8&sensor=false HTTP/1.1\r\n
        Host: maps.google.com:80\r\n
        User-Agent: search4.py\r\n
        Connection: close\r\n
        \r\n"""
urlc=url.encode(encoding="utf-8") #Indispensable pour la socket
def connect_to_google():
    sock = socket.socket()
    sock.connect(('maps.google.com', 80))
    sock.sendall(urlc)
    rawreply = sock.recv(4096)
    print(rawreply)
    
if __name__ == '__main__':
    connect_to_google()