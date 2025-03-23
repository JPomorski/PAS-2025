#!/usr/bin/env python
import socket

HOST = "127.0.0.1"
PORT = 13

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    num1 = input("Enter the first number: ")
    sock.sendto(num1.encode(), server_address)

    op = input("Enter the operator: ")
    sock.sendto(op.encode(), server_address)

    num2 = input("Enter the second number: ")
    sock.sendto(num2.encode(), server_address)

    data = sock.recv(1024).decode()
    print(f"Server response: {data}")

except socket.error as e:
    print(e)

sock.close()
