import socket
import threading

UDP_IP = '127.0.0.1'
UDP_PORT = 5000
MESSAGE = "Python Web development"


def run_client(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_server = ip, port
    for line in MESSAGE.split(' '):
        data = line.encode()
        sock.sendto(data, sock_server)
        print(f'Send data: {data.decode()=} to server: {sock_server=}')
        response, address = sock.recvfrom(1024)
        print(f'Response data: {response.decode()=} from address: {address=}')
    sock.close()


client = threading.Thread(target=run_client, args=(UDP_IP, UDP_PORT))

if __name__ == '__main__':
    client.start()
    client.join()
