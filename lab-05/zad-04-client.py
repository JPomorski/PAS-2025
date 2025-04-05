#!/usr/bin/env python

import socket
import time

HOST = "127.0.0.1"
PORT = 2914

server_address = (HOST, PORT)

try:
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    start = time.time()

    for _ in range(100):
        udp_sock.sendto("PING".encode(), server_address)
        data, _ = udp_sock.recvfrom(1024)

    elapsed = time.time() - start
    print(f"Time elapsed (UDP socket): {elapsed}")

    udp_sock.close()

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    start = time.time()

    for _ in range(100):
        tcp_sock.sendall("PING".encode())
        data = tcp_sock.recv(1024)

    elapsed = time.time() - start
    print(f"Time elapsed (TCP socket): {elapsed}")

    tcp_sock.close()

    # w większości przypadków czas jest zdecydowanie szybszy dla gniazda TCP
    # podejrzewam, że wynika to z bezpośredniego podłączenia pod konkretny adres
    # dzięki czemu gniazdo nie musi tego adresu dodatkowo przetwarzać

    # wadą takiego rozwiązania jest to, że jeśli chcielibyśmy ten adres zmieniać,
    # to musielibyśmy gniazdo co chwila przepinać na nowy adres

    # z drugiej strony dla gniazd UDP ten problem nie istnieje, jakikolwiek adres mu
    # podamy na taki będzie próbował wysłać pakiet

except socket.error as e:
    print(e)
