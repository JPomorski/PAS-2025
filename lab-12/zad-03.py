import socket
import threading
from random import randint

HOST = "127.0.0.1"
PORT = 2412

RANGE = (0, 10)

ROLLED_NUMBER = randint(RANGE[0], RANGE[1])


def handle_client(client_socket, client_address):
    client_info = f"[{client_address[0]}:{client_address[1]}]"

    try:
        while True:
            data = client_socket.recv(1024).decode()
            print(f"{client_info}: {data}")

            try:
                number = int(data)
            except ValueError:
                message = "Given input is not a valid number"
                client_socket.sendall(message.encode())

                continue

            if number < RANGE[0] or number > RANGE[1]:
                message = f"Given number is out of range! Supported range: {RANGE[0]}-{RANGE[1]}"
                client_socket.sendall(message.encode())
            else:
                print(f"{client_info}: Number: {number}, rolled number: {ROLLED_NUMBER}")

                if number < ROLLED_NUMBER:
                    message = "Lower than the rolled number!"
                    client_socket.sendall(message.encode())
                elif number > ROLLED_NUMBER:
                    message = "Higher than the rolled number!"
                    client_socket.sendall(message.encode())
                else:
                    message = "Spot on!"
                    client_socket.sendall(message.encode())

                    client_socket.close()
                    break

    except Exception as e:
        print(e)

    finally:
        client_socket.close()


server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = sock.accept()
    print(f"Connection from {client_address}")

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

    print(f"Active clients: {threading.active_count() - 1}")


