import socket
import threading

UDP_IP = '127.0.0.1'
UDP_PORT = 5000


def run_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_server = ip, port
    sock.bind(sock_server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(f'Received data: {data.decode()=} from: {address=}')
            sock.sendto(data, address)
            print(f'Send data: {data.decode()=} to: {address=}')

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


server = threading.Thread(target=run_server, args=(UDP_IP, UDP_PORT))

if __name__ == '__main__':
    server.start()
    server.join()
