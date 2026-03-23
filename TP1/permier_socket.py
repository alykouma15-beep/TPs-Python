from ast import main
import http.client
def connect_to_google():
    path = ('/maps/geo?g=207+N.+Defiancet+St%2C+Anchbo1d%2C+0H&output=json&oe=utf8')
    connection = http.client.HTTPConnection('maps.google.com')
    connection.request('GET', path)
    rawreply = connection.getresponse().read()
    print(rawreply)

if __name__ == '__main__':
    connect_to_google()