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
        hostname, address = sock.recvfrom(4096)

        try:
            ip_address = socket.gethostbyname(hostname)
            sock.sendto(ip_address.encode(), address)
        except socket.error as e:
            sock.sendto(f"Failed retrieving hostname: {e}".encode(), address)
            print(e)

    except Exception as e:
        print(e)
