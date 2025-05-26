import socket
from time import sleep

HOST = "127.0.0.1"
PORT = 2412

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    message = "Hello :3333"

    while True:
        sock.sendall(message.encode())

        data = sock.recv(1024)
        print(f"Server response: {data.decode()}")

        sleep(5)

except socket.error as e:
    print(e)

sock.close()
