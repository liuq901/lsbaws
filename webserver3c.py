from multiprocessing import Process
import os
import socket
import time

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5

def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(request.decode())
    http_response = b'HTTP/1.1 200 OK\n\nHello, World!\n'
    client_connection.sendall(http_response)
    time.sleep(3)

def fork(listen_socket, client_connection):
    listen_socket.close()
    handle_request(client_connection)
    client_connection.close()

def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print(f'Serving HTTP on port {PORT} ...')
    print(f'Parent PID (PPID): {os.getpid()}\n')

    while True:
        client_connection, client_address = listen_socket.accept()
        p = Process(target=fork, args=(listen_socket, client_connection))
        p.start()
        client_connection.close()

if __name__ == '__main__':
    serve_forever()
