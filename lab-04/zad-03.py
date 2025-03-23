#!/usr/bin/env python
import socket

HOST = "127.0.0.1"
PORT = 13

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"Server listening on {HOST}:{PORT}")

while True:
    try:
        data, addr = sock.recvfrom(1024)
        if data:
            sock.sendto(data, addr)

    except Exception as e:
        print(e)
