import json
import logging
import os
import socket
import urllib.parse
from datetime import datetime

UDP_IP = '127.0.0.1'
UDP_PORT = 5000

storage = 'storage'
data_json = 'data.json'


def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_server = UDP_IP, UDP_PORT
    sock.bind(sock_server)
    logging.debug(f'{sock_server=}')
    try:
        while True:
            data, address = sock.recvfrom(1024)
            data_parse = urllib.parse.unquote_plus(data.decode())
            data_dict: dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
            isExist = os.path.exists(os.path.join(storage, data_json))
            match isExist:
                case True:
                    with open(os.path.join(storage, data_json), 'r') as fh:
                        data_storage = json.load(fh)
                        data_storage.update({str(datetime.now()): data_dict})
                    with open(os.path.join(storage, data_json), 'w') as fh:
                        json.dump(data_storage, fh, indent=4)
                case False:
                    os.mkdir(storage)
                    with open(os.path.join(storage, data_json), 'w') as fh:
                        json.dump(dict({str(datetime.now()): data_dict}), fh, indent=4)
    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()
