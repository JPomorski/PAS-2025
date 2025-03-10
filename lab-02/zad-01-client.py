#!/usr/bin/env python
import socket

# HOST = "ntp.task.gda.pl"
HOST = "127.0.0.1"
PORT = 13

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    server_time = sock.recv(1024).decode()
    print(f"Received time: {server_time}")

except socket.error as e:
    print(e)

sock.close()
