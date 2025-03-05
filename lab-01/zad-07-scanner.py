#!/usr/bin/env python
import socket


def scan_range(host, min_port, max_port):
    open_ports = []

    for port in range(min_port, max_port + 1):
        server_address = (host, port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect(server_address)
            open_ports.append(port)

        except socket.error:
            print(f"Port {port} not open")

        sock.close()

    print(f"Open ports found: {open_ports}")


# HOST = '127.0.0.1'

HOST = input("Enter host IP or hostname: ")
scan_range(HOST, 2900, 2920)
