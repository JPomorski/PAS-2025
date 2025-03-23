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
        ip, address = sock.recvfrom(4096)

        try:
            hostname_info = socket.gethostbyaddr(ip)
            sock.sendto(hostname_info[0].encode(), address)
        except socket.error as e:
            sock.sendto(f"Failed retrieving hostname: {e}".encode(), address)
            print(e)

    except Exception as e:
        print(e)
