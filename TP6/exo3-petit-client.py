from Exo1_2requete_response import *
import argparse

def main(v):
    dem=httpclient("GET",v,'1')

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    s.connect(("127.0.0.1",80))
    s.sendall(dem.encode('utf-8'))
    print("envoyé")
    print(json.loads(s.recv(1024).decode('utf-8')))
    
    
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("type")
    args=parser.parse_args()
    h=args.type
    main(h)