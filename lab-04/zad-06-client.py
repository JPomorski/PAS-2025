#!/usr/bin/env python
import socket

HOST = "127.0.0.1"
PORT = 13

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

hostname = input("Enter hostname: ")

try:
    sock.sendto(hostname.encode(), server_address)

    data = sock.recv(1024).decode()
    print(f"Server response: {data}")

except socket.error as e:
    print(e)
