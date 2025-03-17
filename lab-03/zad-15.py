#!/usr/bin/env python
import socket


def get_bytes(array, size, start_pos):
    return array[start_pos:start_pos+size]


datagram = '''45 00 00 4e f7 fa 40 00 38 06 9d 33 d4 b6 18 1b
c0 a8 00 02 0b 54 b9 a6 fb f9 3c 57 c1 0a 06 c1
80 18 00 e3 ce 9c 00 00 01 01 08 0a 03 a6 eb 01
00 0b f8 e5 6e 65 74 77 6f 72 6b 20 70 72 6f 67
72 61 6d 6d 69 6e 67 20 69 73 20 66 75 6e'''

data_bytes = datagram.replace('\n', ' ').split(' ')
print(data_bytes)

version = get_bytes(data_bytes, 1, 0)
version = int("".join(version), 16) >> 4
print(version)

source_address = get_bytes(data_bytes, 4, 12)
destination_address = get_bytes(data_bytes, 4, 16)
protocol_type = get_bytes(data_bytes, 1, 9)

source_address = ".".join([str(int(address, 16)) for address in source_address])
destination_address = ".".join([str(int(address, 16)) for address in destination_address])
protocol_type = int("".join(protocol_type), 16)
print(protocol_type)

source_port = get_bytes(data_bytes, 2, 20)
destination_port = get_bytes(data_bytes, 2, 22)
data = data_bytes[52:]

source_port = int("".join(source_port), 16)
destination_port = int("".join(destination_port), 16)
data = bytes.fromhex("".join(data)).decode()

print(source_address, destination_address, data)

# HOST = "212.182.24.27"
HOST = "127.0.0.1"
PORT = 2911
server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    message = f"zad15odpA;ver;{version};srcip;{source_address};dstip;{destination_address};type;{protocol_type}"
    print(message)

    sock.sendto(message.encode(), server_address)

    recv_data, _ = sock.recvfrom(1024)
    response = recv_data.decode()

    print(f"Server response: {response}")

    if response == "TAK":
        message = f"zad15odpB;srcport;{source_port};dstport;{destination_port};data;{data}"
        print(message)

        sock.sendto(message.encode(), server_address)

        recv_data, _ = sock.recvfrom(1024)
        print(f"Server response: {recv_data.decode()}")

except socket.error as e:
    print(e)

sock.close()
