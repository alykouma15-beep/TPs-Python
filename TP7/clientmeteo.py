import argparse
from http.client import HTTPSConnection
from urllib.parse import quote

def main(v):
    conn=HTTPSConnection("api.openweathermap.org")
    conn.request('GET',f"/data/2.5/weather?q={quote(v)}&appid=6a14331c45f201c716239059aafb1a3c")
    print("envoyé")
    response=conn.getresponse()
    print(response.status,response.reason)
    print(response.readlines())
    conn.close()
if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Indiquez la route voulue en argument")
    parser.add_argument("ville")
    args=parser.parse_args()
    h=args.ville
    main(h)