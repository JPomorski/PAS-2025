import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 2412

filename = "server_log.txt"

lock = threading.Lock()


def write_to_file(message):
    print(message)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stamped_message = f"[{timestamp}]: {message}\n"

    with lock:
        with open(filename, "a") as f:
            f.write(stamped_message)


def handle_client(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024)

            if data:
                write_to_file(f"{client_address[0]}:{client_address[1]}: {data.decode()}")
                client_socket.sendall(data)

    except Exception as e:
        print(e)

    finally:
        client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen()

write_to_file(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    write_to_file(f"Connection from {client_address}")

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

    write_to_file(f"Active clients: {threading.active_count() - 1}")

