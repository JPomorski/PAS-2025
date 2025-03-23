#!/usr/bin/env python
import socket

# HOST = "212.182.24.27"
HOST = "127.0.0.1"
PORT = 2900

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    message = input("Enter message to send: ")
    sock.sendto(message.encode("utf-8"), server_address)
    print(f"Message sent: {message}")

    data, _ = sock.recvfrom(1024)
    print(f"Server response: {data.decode()}")

except socket.error as e:
    print(e)

sock.close()
