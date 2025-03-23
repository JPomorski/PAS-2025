#!/usr/bin/env python
import socket

HOST = "127.0.0.1"
PORT = 13

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen(1)

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = sock.accept()
    print(f"Connection from {client_address}")

    try:
        data, addr = client_socket.recvfrom(1024)
        if data:
            client_socket.sendall(data)

    except Exception as e:
        print(e)
