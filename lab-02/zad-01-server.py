#!/usr/bin/env python
import socket
import time

# HOST = "ntp.task.gda.pl"
HOST = "127.0.0.1"
PORT = 13

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen(1)

print(f"NTP server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = sock.accept()

    try:
        print(f"Connection from {client_address}")

        timestamp = int(time.time())
        current_time = time.ctime(timestamp)
        client_socket.sendall(current_time.encode("utf-8"))

    except Exception as e:
        print(e)

    finally:
        client_socket.close()
