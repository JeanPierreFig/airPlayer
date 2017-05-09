

from http.server import HTTPServer, CGIHTTPRequestHandler # Python 3
import threading

server = HTTPServer(('', 8000), CGIHTTPRequestHandler)

def start():

       server.serve_forever()


def fin():
    server.shutdown()
    print('shutdown')

print('server running on port {}'.format(server.server_port))