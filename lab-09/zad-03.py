import socket

HOST = "progress.ski"
PORT = 80

PATH = "/image.jpg"


def receive_all(sock):
    response = b""

    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break

        response += chunk

    return response


server_address = (HOST, PORT)

range_end = 1023

request = (
    f"GET {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Accept: image/jpg\r\n"
    "Connection: close\r\n\r\n"
)

# Jeśli serwer udostępnia nagłówek "Transfer-Encoding: chunked", to automatycznie
# wysyła obrazek w kawałkach i można by go odebrać odpowiednio parsując odpowiedź.

# Ponieważ jednak ten serwer tego nie robi, pobieramy obrazek całościowo, aby poznać
# jego rozmiar, a następnie odbieramy go ponownie, ręcznie dzieląc na kawałki.

# Służy do tego nagłówek "Range", który dodatkowo zwraca nam w odpowiedzi
# nagłówek "Content-Range", zawierający zakres odczytanych danych.

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    sock.sendall(request.encode())

    data = receive_all(sock)

    response_end = data.find(b"\r\n\r\n")
    html_headers = data[:response_end].decode()

    content_length = 0

    for line in html_headers.splitlines():
        if line.startswith("Content-Length"):
            content_length = int(line.split(":")[1])

    print(f"Server response: {html_headers}")

    html_body = data[response_end + 4:]
    print(html_body)

    image_data = b""

    chunk_size = content_length // 3

    chunk_start = 0
    chunk_end = chunk_size

    sock.close()

    for i in range(3):
        if i == 2:
            chunk_end = content_length - 1

        print()

        request = (
            f"GET {PATH} HTTP/1.1\r\n"
            f"Host: {HOST}\r\n"
            "Accept: image/jpg\r\n"
            f"Range: bytes={chunk_start}-{chunk_end}\r\n"
            "Connection: close\r\n\r\n"
        )

        print(request)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect(server_address)

        sock.sendall(request.encode())

        data = receive_all(sock)

        response_end = data.find(b"\r\n\r\n")
        html_headers = data[:response_end].decode()

        print(f"Server response: {html_headers}")

        html_body = data[response_end + 4:]
        print(html_body)

        image_data += html_body

        chunk_start = chunk_end + 1
        chunk_end += chunk_size

    with open("image.jpg", "wb") as f:
        f.write(image_data)

except Exception as e:
    print(e)
