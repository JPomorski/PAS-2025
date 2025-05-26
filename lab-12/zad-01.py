import socket
import threading

HOST = "127.0.0.1"
PORT = 2412


def handle_client(client_socket, client_address):
    try:
        while True:
            data = client_socket.recv(1024)

            if data:
                print(f"{client_address[0]}:{client_address[1]}: {data.decode()}")
                client_socket.sendall(data)

    except Exception as e:
        print(e)

    finally:
        client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()

    print(f"Active clients: {threading.active_count() - 1}")
