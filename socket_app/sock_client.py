import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 5000


def run_client(data: bytes):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = UDP_IP, UDP_PORT
    sock.sendto(data, server)
    sock.close()
