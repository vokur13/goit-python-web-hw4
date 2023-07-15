import logging
import threading

from http_handler import run
from socket_app import run_server

server = threading.Thread(target=run_server)  # Socket-server
client = threading.Thread(target=run)  # HTTP-server

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    server.start()
    client.start()
    server.join()
    client.join()
