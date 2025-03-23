#!/usr/bin/env python
import socket
import time
from datetime import datetime

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
        data, _ = client_socket.recvfrom(1024)

        timestamp = int(time.time())
        current_time = time.ctime(timestamp)
        date_time = datetime.now()

        message = f"Current date and time: {date_time}"
        client_socket.sendall(message.encode())

    except Exception as e:
        print(e)

    finally:
        client_socket.close()
