#!/usr/bin/env python
import socket


def check_message_length(msg, max_length, allow_oversize):
    if len(msg) < max_length:
        msg += " " * (max_length - len(msg))
    elif len(msg) > max_length:
        if not allow_oversize:
            msg = msg[:max_length]

    return msg


# HOST = "212.182.24.27"
HOST = "127.0.0.1"
PORT = 2908
MAX_PACKET_LENGTH = 20

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    message = input("Enter message to send: ")
    message = check_message_length(message, MAX_PACKET_LENGTH, True)

    sock.sendto(message.encode(), server_address)
    print(f"Message sent: {message}")

    data, _ = sock.recvfrom(1024)
    print(f"Server response: {data.decode()}")

except socket.error as e:
    print(e)

sock.close()
