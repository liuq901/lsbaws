import errno
import multiprocessing
from multiprocessing import Process
import socket
import time

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5

def grim_reaper(pid, exitcode):
    print(f'Child {pid} terminated with status {exitcode}\n')

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

    all_process = set()
    while True:
        try:
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            code, msg = e.args
            if code == errno.EINTR:
                continue
            else:
                raise

        p = Process(target=fork, args=(listen_socket, client_connection))
        all_process.add(p)
        p.start()
        client_connection.close()
        active_process = set(multiprocessing.active_children())
        end_process = all_process - active_process
        for process in end_process:
            all_process.remove(process)
            grim_reaper(process.pid, process.exitcode)

if __name__ == '__main__':
    serve_forever()
