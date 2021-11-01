import argparse
from multiprocessing import Process
import socket

SERVER_ADDRESS = 'localhost', 8888
REQUEST = b'GET /hello HTTP/1.1\nHost: localhost:8888\n\n'

def fork(max_conns):
    for connection_num in range(max_conns):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVER_ADDRESS)
        sock.sendall(REQUEST)
        print(connection_num)

def main(max_clients, max_conns):
    socks = []
    for client_num in range(max_clients):
        p = Process(target=fork, args=(max_conns,))
        p.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Test client for LSBAWS.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--max-conns',
        type=int,
        default=1024,
        help='Maximum number of connections per client.'
    )
    parser.add_argument(
        '--max-clients',
        type=int,
        default=1,
        help='Maximum number of clients.'
    )
    args = parser.parse_args()
    main(args.max_clients, args.max_conns)
