#!/usr/bin/env python

import socket
import sys
from time import gmtime, strftime

HOST = '127.0.0.1'
PORT = 2908
MAX_PACKET_LENGTH = 20


def recv_all(sock, message_length):
    message = ""
    bytes_received = 0

    while bytes_received < message_length:

        chunk = sock.recv(message_length - bytes_received)

        if not chunk:
            break

        bytes_received += len(chunk)
        message += chunk

    return message


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

s.listen(1000)

print("[%s] TCP ECHO Server is waiting for incoming connections ... " % strftime("%Y-%m-%d %H:%M:%S", gmtime()))

while True:

    connection, client_address = s.accept()

    try:
        print("[%s] Client %s connected ... " % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address))

        while True:
            try:
                data = recv_all(connection, MAX_PACKET_LENGTH)
                print("[%s] Client %s sent \'%s\' " % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address, data))

                if data:
                    print("[%s] Sending back to client %s ... " % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), data))
                    connection.sendall(data.encode())
                else:
                    print("[%s] Client %s disconnected ... " % (strftime("%Y-%m-%d %H:%M:%S", gmtime()), client_address))
                    break

            except socket.error as e:
                print("[%s] Something happened, but I do not want to bother you ... %s " % (
                    strftime("%Y-%m-%d %H:%M:%S", gmtime()), e)
                )

    finally:
        connection.close()
