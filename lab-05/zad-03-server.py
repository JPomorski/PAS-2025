#!/usr/bin/env python

import socket

HOST = "127.0.0.1"
TCP_PORT = 2913

server_address = (HOST, TCP_PORT)

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

udp_ports = [13666, 25666, 11666]


while True:
    for udp_port in udp_ports:
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind((HOST, udp_port))

        print(f"Server listening on {HOST}:{udp_port}")

        while True:
            data, addr = udp_sock.recvfrom(1024)

            if data:
                print(data)
            if data.decode() == "PING":
                print("PONG")
                udp_sock.sendto("PONG".encode(), addr)
                break

    tcp_sock.bind((HOST, TCP_PORT))

    tcp_sock.listen(0)

    client_socket, client_address = tcp_sock.accept()
    print(f"Connection from {client_address}")

    try:
        message = "Congratulations! You found the hidden."
        client_socket.sendall(message.encode())

    except Exception as e:
        print(e)

    finally:
        client_socket.close()
