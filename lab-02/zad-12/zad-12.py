#!/usr/bin/env python
import socket


def check_message_length(msg, max_length, allow_oversize):
    if len(msg) < max_length:
        msg += " " * (max_length - len(msg))
    elif len(msg) > max_length:
        if not allow_oversize:
            msg = msg[:max_length]

    return msg


def send_all(msg, sock, message_length):
    message = msg.encode()
    bytes_sent = 0

    while bytes_sent < message_length:

        sent = sock.send(message[bytes_sent:])

        if not sent:
            break

        bytes_sent += sent


def recv_all(sock, message_length):
    message = ""
    bytes_received = 0

    while bytes_received < message_length:

        chunk = sock.recv(message_length - bytes_received)

        if not chunk:
            break

        bytes_received += len(chunk)
        message += chunk.decode()

    return message


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

    # send_all(message, sock, MAX_PACKET_LENGTH)
    sock.sendall(message.encode())
    print(f"Message sent: {message}")

    data = recv_all(sock, MAX_PACKET_LENGTH)
    print(f"Server response: {data}")

except socket.error as e:
    print(e)

sock.close()
