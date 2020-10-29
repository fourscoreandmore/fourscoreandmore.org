from app import app
import os
from gevent.pywsgi import WSGIServer

if __name__ == "__main__":
    http_server = WSGIServer(('127.0.0.1', int(os.environ["PORT"])), app)
    http_server.serve_forever()
