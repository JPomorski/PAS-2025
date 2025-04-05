#!/usr/bin/env python
import socket


def get_bytes(array, size, start_pos):
    return array[start_pos:start_pos+size]


datagram = '''0b 54 89 8b 1f 9a 18 ec bb b1 64 f2 80 18
00 e3 67 71 00 00 01 01 08 0a 02 c1 a4 ee
00 1a 4c ee 68 65 6c 6c 6f 20 3a 29'''

data_bytes = datagram.replace('\n', ' ').split(' ')
print(data_bytes)

source_port = get_bytes(data_bytes, 2, 0)
destination_port = get_bytes(data_bytes, 2, 2)
data = data_bytes[32:]

source_port = int("".join(source_port), 16)
destination_port = int("".join(destination_port), 16)
data = bytes.fromhex("".join(data)).decode()

print(source_port, destination_port, data)

message = f"zad13odp;src;{source_port};dst;{destination_port};data;{data}"
print(message)

# HOST = "212.182.24.27"
HOST = "127.0.0.1"
PORT = 2909
server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.sendto(message.encode(), server_address)

    data, _ = sock.recvfrom(1024)
    print(f"Server response: {data.decode()}")

except socket.error as e:
    print(e)

sock.close()

