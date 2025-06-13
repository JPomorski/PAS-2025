import socket
import random

HOST = "127.0.0.1"
PORT = 2904


filenames = [
    "Brr-Brr-Patapim.jpg",
    "Cappuccino-Assassino.jpg",
    "Chimpanzini-Bananini.jpg",
    "Giraffa-Celeste.jpg",
    "Lirili-Larila.jpg"
]


def receive_exact(sock, n):
    message = b''

    while len(message) < n:
        chunk = sock.recv(1024)

        if not chunk:
            break

        message += chunk

    return message


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    try:
        while True:
            data = client_socket.recv(1024).decode()

            if not data:
                break

            print(f"Received message: {data}")

            args = data.split(" ")

            print(args)

            filename = "zad-03-images/"

            if args[0] == "GET_IMAGE":
                if args[1] != "\r\n":
                    filename += args[1]
                else:
                    filename += random.choice(filenames)

                with open(filename, "rb") as f:
                    file_data = f.read()

                size = len(file_data)

                response = f"SIZE {size} NAME {filename} \r\n"
                client_socket.sendall(response.encode())
                client_socket.sendall(file_data)

            elif args[0] == "GET_FILE_LIST":
                response = "FILE LIST \r\n"
                response += f"{'\r\n'.join(filenames)} \r\n"
                client_socket.sendall(response.encode())

            else:
                response = f"ERROR \r\n"
                client_socket.sendall(response.encode())

    except Exception as e:
        print(e)

    finally:
        client_socket.close()
