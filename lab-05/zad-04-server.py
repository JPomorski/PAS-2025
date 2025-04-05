#!/usr/bin/env python

import socket

HOST = "127.0.0.1"
PORT = 2914

server_address = (HOST, PORT)

while True:
    try:
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind(server_address)

        print(f"Server listening on {HOST}:{PORT}")

        for _ in range(100):
            data, addr = udp_sock.recvfrom(1024)
            udp_sock.sendto(data, addr)

        udp_sock.close()

        tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_sock.bind(server_address)

        tcp_sock.listen(0)

        client_socket, client_address = tcp_sock.accept()
        print(f"Connection from {client_address}")

        for _ in range(100):
            data = client_socket.recv(1024)
            client_socket.sendall(data)

        client_socket.close()

    except Exception as e:
        print(e)
