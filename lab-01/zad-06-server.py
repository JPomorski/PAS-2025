#!/usr/bin/env python
import socket

HOST = '127.0.0.1'
PORT = 2904

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()

    try:
        print(f"Connection from {client_address}")

    except Exception as e:
        print(e)

    finally:
        client_socket.close()
