#!/usr/bin/env python

import socket

HOST = "127.0.0.1"
PORT = 2913

server_address = (HOST, PORT)
udp_ports = []
found_ports = 0

starting_port = 666

try:
    udp_port = starting_port

    while found_ports < 3:
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_address = (HOST, udp_port)

        print(f"Knocking at {HOST} at port {udp_port}")

        try:
            udp_sock.sendto("PING".encode(), udp_address)
            data, _ = udp_sock.recvfrom(1024)

            print(f"Server response: {data}")

            if data.decode() == "PONG":
                print("Open UDP port found")
                udp_ports.append(udp_port)
                found_ports += 1
                udp_port = starting_port
            else:
                udp_sock.close()
                udp_port += 1000
        except socket.error:
            udp_port += 1000

    print(f"Found open UDP ports: {udp_ports}")

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    data = tcp_sock.recv(1024)
    print(f"Server response: {data}")

except socket.error as e:
    print(e)
