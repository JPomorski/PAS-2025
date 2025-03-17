#!/usr/bin/env python
import socket


def get_bytes(array, size, start_pos):
    return array[start_pos:start_pos+size]


datagram = '''ed 74 0b 55 00 24 ef fd 70 72 6f 67 72 61
6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f
6e 20 69 73 20 66 75 6e'''

data_bytes = datagram.replace('\n', ' ').split(' ')
print(data_bytes)

source_port = get_bytes(data_bytes, 2, 0)
destination_port = get_bytes(data_bytes, 2, 2)
data = data_bytes[8:]

source_port = int("".join(source_port), 16)
destination_port = int("".join(destination_port), 16)
data = bytes.fromhex("".join(data)).decode()

print(source_port, destination_port, data)

message = f"zad14odp;src;{source_port};dst;{destination_port};data;{data}"
print(message)

# HOST = "212.182.24.27"
HOST = "127.0.0.1"
PORT = 2910
server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.sendto(message.encode(), server_address)

    data, _ = sock.recvfrom(1024)
    print(f"Server response: {data.decode()}")

except socket.error as e:
    print(e)

sock.close()

