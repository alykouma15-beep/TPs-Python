from json import JSONDecodeError
from socket import AF_INET
from ssl import SOCK_STREAM
import http.server

class Traiteurget(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/home":
            self.send_response(200,"OK")
            self.send_header("Content-type","test/plain")
            with open("index.html") as f:
                f=f.read()
                self.wfile.write(f.encode('utf-8'))
        else:
            self.send_response(404,"NOT FOUND")
            self.send_header("Content-type","test/plain")
            with open("notfound.html") as f:
                f=f.read()
                self.wfile.write(f.encode('utf-8'))
            
def main():
    print("seveur en ecoute")
    server1=http.server.HTTPServer(("127.0.0.1",80),Traiteurget)
    server1.serve_forever()


if __name__=="__main__":
    main()