import socket

HOST = "127.0.0.1"
PORT = 2904


def receive_exact(sock, n):
    message = b''

    while len(message) < n:
        chunk = sock.recv(1024)

        if not chunk:
            break

        message += chunk

    return message


def save_file(data):
    args = data.split(" ")

    filename = "zad-02-received/"
    filename += args[3].split("/")[1]

    size = args[1]

    file_data = receive_exact(sock, int(size))

    with open(filename, "wb") as f:
        f.write(file_data)


server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    message = "GET_IMAGE \r\n"
    sock.sendall(message.encode())

    data = sock.recv(1024).decode()
    print(f"Server response: {data}")

    save_file(data)

    message = "HELLO \r\n"
    sock.sendall(message.encode())

    data = sock.recv(1024).decode()
    print(f"Server response: {data}")

    message = "GET_FILE_LIST \r\n"
    sock.sendall(message.encode())

    data = sock.recv(1024).decode()
    print(f"Server response: {data}")

    message = "GET_IMAGE Lirili-Larila.jpg \r\n"
    sock.sendall(message.encode())

    data = sock.recv(1024).decode()
    print(f"Server response: {data}")

    save_file(data)

except Exception as e:
    print(e)
