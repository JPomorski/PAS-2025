import socket
from random import randint
from time import sleep

HOST = "127.0.0.1"
PORT = 2412

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    number = "aaaa"
    sock.sendall(number.encode())

    data = sock.recv(1024).decode()
    print(f"Server response: {data}")

    while True:
        number = str(randint(0, 10))
        print(f"Random number: {number}")

        sock.sendall(number.encode())

        data = sock.recv(1024).decode()
        print(f"Server response: {data}")

        if data == "Spot on!":
            break

        sleep(5)

except socket.error as e:
    print(e)

sock.close()
