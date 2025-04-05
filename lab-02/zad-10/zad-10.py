#!/usr/bin/env python
import socket

# HOST = "212.182.24.27"
HOST = "127.0.0.1"
PORT = 2907

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    message = input("Enter hostname to send: ")
    sock.sendto(message.encode("utf-8"), server_address)

    data, _ = sock.recvfrom(1024)
    print(f"Server response: {data.decode()}")

except socket.error as e:
    print(e)

sock.close()
