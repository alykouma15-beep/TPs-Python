from Exo1_2requete_response import *
import argparse
from http.client import HTTPConnection

def main(v):
    conn=HTTPConnection("127.0.0.1",80)
    conn.request('GET',v)
    print("envoyé")
    response=conn.getresponse()
    print(response.status,response.reason)
    print(response.readlines())
    conn.close()
if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Indiquez la route voulue en argument")
    parser.add_argument("chemin")
    args=parser.parse_args()
    h=args.chemin
    main(h)