import socket

HOST = "127.0.0.1"
PORT = 8080

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen(1)

# Działa elegancko w przeglądarce

print(f"HTTP server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = sock.accept()

    print(f"Connection from {client_address}")

    try:
        request = client_socket.recv(1024).decode()
        print(request)

        request_lines = request.splitlines()
        first_line = request_lines[0].strip().split()

        if len(first_line) != 3:
            with open("400.html") as f:
                body = f.read()

            response_headers = (
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Connection: close\r\n\r\n"
            )

            response = response_headers.encode() + body.encode()

            client_socket.sendall(response)

            continue

        path = first_line[1]

        if path == "/" or path == "/index.html":
            with open("index.html") as f:
                body = f.read()

            response_headers = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Connection: close\r\n\r\n"
            )

            response = response_headers.encode() + body.encode()
            client_socket.sendall(response)

        else:
            with open("404.html") as f:
                body = f.read()

            response_headers = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Connection: close\r\n\r\n"
            )

            response = response_headers.encode() + body.encode()

            client_socket.sendall(response)

    except Exception as e:
        print(e)

    finally:
        client_socket.close()
