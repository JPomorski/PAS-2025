import socket

HOST = "127.0.0.1"
PORT = 2413


def receive_exact(sock, n):
    message = b''

    while len(message) < n:
        chunk = sock.recv(1024)

        if not chunk:
            break

        message += chunk

    return message


def receive_headers(sock):
    headers = b''

    while True:
        chunk = sock.recv(1024)

        if not chunk:
            break

        headers += chunk

        if b"\r\n\r\n" in chunk:
            break

    return headers


def parse_file_data(headers):
    filename, size = None, None

    for header in headers.splitlines():
        if header.startswith("Filename:"):
            filename = header.split(":")[1].strip()
        if header.startswith("Size:"):
            size = int(header.split(":")[1].strip())

    return filename, size


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

            if data == "HELLO AUTHORIZE":
                response = f"HELLO FROM {HOST}:{PORT} - AUTHORIZED"
                client_socket.send(response.encode())

                while True:
                    data = client_socket.recv(1024).decode()

                    if not data:
                        break

                    print(f"Received message: {data}")

                    if data == "SEND FILE":
                        response = "OK SERVER READY"
                        client_socket.send(response.encode())

                        headers = receive_headers(client_socket).decode()

                        if not headers:
                            break

                        print(f"Received message: {headers}")

                        filename, size = parse_file_data(headers)

                        file_data = receive_exact(client_socket, size)
                        print(file_data[:50])

                        response = "OK FILE RECEIVED"
                        client_socket.sendall(response.encode())

                        try:
                            file_format = f".{filename.split(".")[1]}"
                            filename = f"{filename.split(".")[0]}-received"

                            print(f"Filename: {filename}")
                            print(f"File format: {file_format}")
                            print(f"File size: {size}")
                            print(f"File data: {file_data[:50]}")

                            with open(f"{filename}{file_format}", "wb") as f:
                                f.write(file_data)
                                response = "OK FILE SAVED"
                                client_socket.send(response.encode())

                        except Exception as e:
                            print(e)
                            response = f"ERROR WHEN SAVING FILE: {e}"
                            client_socket.send(response.encode())

                    else:
                        response = "ERROR: UNKNOWN COMMAND"
                        client_socket.sendall(response.encode())

            else:
                response = f"HELLO PLEASE AUTHORIZE BEFORE PROCEEDING"
                client_socket.send(response.encode())

    except Exception as e:
        print(e)

    finally:
        client_socket.close()
