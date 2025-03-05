#!/usr/bin/env python
import socket

# HOST = '127.0.0.1'
# PORT = 2904

HOST = input("Enter host IP or hostname: ")
PORT = int(input("Enter port: "))
server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

except socket.error as e:
    print(e)

sock.close()
