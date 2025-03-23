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
        data1, address = sock.recvfrom(4096)
        op, _ = sock.recvfrom(4096)
        data2, _ = sock.recvfrom(4096)

        if data1 and data2 and op:
            op = str(op.decode())
            data1 = data1.decode()
            data2 = data2.decode()

            result = ""

            try:
                if op == '+':
                    result = float(data1) + float(data2)
                elif op == '-':
                    result = float(data1) - float(data2)
                elif op == '*':
                    result = float(data1) * float(data2)
                elif op == '/':
                    result = float(data1) / float(data2)
                else:
                    result = "Bad operator. I support only +, -, *, / math operators"

                sent = sock.sendto(str(result).encode(), address)

            except ValueError as e:
                print(e)

    except Exception as e:
        print(e)
