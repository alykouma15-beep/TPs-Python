from json import JSONDecodeError
from os import read
import readline
from socket import AF_INET
from ssl import SOCK_STREAM
from Exo1_2requete_response import *

class Server:
    def __init__(self,host,port):
        self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.s.bind((host,port))
        
    def traiterget(self,req):
        if req["type"]!="GET": raise TypeError("Pas de GET")
        if req['url']!="/home": return 404
        return "200 OK"


def main():
    server1=Server("127.0.0.1",80)
    server1.s.listen(5)
    print("seveur en ecoute")
    while True:
        c,addr=server1.s.accept()
        try:
            requete=json.loads(c.recv(1024).decode('utf-8')) 
        except JSONDecodeError:
            fichier=open('notfound.html').readlines()
            res=httpresponse('1','404',str(fichier))
            c.sendall(res.encode('utf-8'))
        print(requete)#reception du get
        status=server1.traiterget(requete)
        if isinstance(status,str):
            fichier=open("index.html").readlines()
            res=httpresponse('1',status,str(fichier),requete["headers"])
        
        else:
            fichier=open('notfound.html').readlines()
            res=httpresponse('1',status,str(fichier),requete["headers"])

        c.sendall(res.encode('utf-8'))
        print("finish")
    





if __name__=="__main__":
    main()