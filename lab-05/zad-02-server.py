#!/usr/bin/env python

import socket
from random import randint

HOST = "127.0.0.1"
PORT = 2912
RANGE = (1, 10)

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen(1)

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = sock.accept()
    print(f"Connection from {client_address}")

    try:
        data, address = client_socket.recvfrom(4096)
        try:
            number = int(data)
        except ValueError:
            message = "Given input is not a valid number"
            client_socket.sendall(message.encode())

            client_socket.close()
            continue

        if number < RANGE[0] or number > RANGE[1]:
            message = f"Given number is out of range! Supported range: {RANGE[0]}-{RANGE[1]}"
            client_socket.sendall(message.encode())
        else:
            rolled_number = randint(RANGE[0], RANGE[1])

            print(f"Number: {number}, Rolled number: {rolled_number}")

            if number < rolled_number:
                message = "Lower than the rolled number!"
                client_socket.sendall(message.encode())
            elif number > rolled_number:
                message = "Higher than the rolled number!"
                client_socket.sendall(message.encode())
            else:
                message = "Spot on!"
                client_socket.sendall(message.encode())

                client_socket.close()
                break

    except Exception as e:
        print(e)

    finally:
        client_socket.close()
