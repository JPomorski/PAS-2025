#!/usr/bin/env python
import socket


def recv_all(sock, message_length):
    message = ""
    bytes_received = 0

    while bytes_received < message_length:

        chunk = sock.recv(message_length - bytes_received)

        if not chunk:
            break

        bytes_received += len(chunk)
        message += str(chunk)

    return message


# HOST = "212.182.24.27"
HOST = "127.0.0.1"
PORT = 2900
MAX_PACKET_LENGTH = 20

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen(1)

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = sock.accept()
    print(f"Connection from {client_address}")

    try:
        data = recv_all(client_socket, MAX_PACKET_LENGTH)
        if data:
            client_socket.sendall(data.encode())

    except Exception as e:
        print(e)
