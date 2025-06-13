import socket

HOST = "127.0.0.1"
PORT = 2413


def send_message(sock, message):
    sock.sendall(message.encode())

    data = sock.recv(1024)
    print(f"Server response: {data.decode()}")

    return data


def verify_server_response():
    data = sock.recv(1024).decode()
    print(f"Server response: {data}")

    if data.startswith("OK"):
        data = sock.recv(1024).decode()
        print(f"Server response: {data}")

        if data.startswith("OK"):
            print("File has been saved successfully")
        else:
            print("Operation failed")
    else:
        print("Operation failed")


server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    send_message(sock, "Hello")

    send_message(sock, "HELLO AUTHORIZE")

    send_message(sock, "BAJO JAJO")

    send_message(sock, "SEND FILE")

    filename = "sahur.png"

    with open(filename, "rb") as f:
        file_data = f.read()
        headers = (
            f"SENDING FILE\r\n"
            f"Filename: {filename}\r\n"
            f"Size: {len(file_data)}\r\n"
            f"Content:\r\n\r\n"
        )

        sock.sendall(headers.encode())
        sock.sendall(file_data)

    verify_server_response()

    # Błędne polecenie:

    send_message(sock, "SEND FILE")

    headers = (
        f"SENDING FILE\r\n"
        f"Filename: ?\r\n"
        f"Size: {len(file_data)}\r\n"
        f"Content:\r\n\r\n"
    )

    sock.sendall(headers.encode())
    sock.sendall(file_data)

    verify_server_response()

    send_message(sock, "BAJO JAJO")

except Exception as e:
    print(e)
