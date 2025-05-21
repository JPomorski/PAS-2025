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

# Aby pozyskać informację o ostatniej modyfikacji pliku
# można wykorzystać nagłówek odpowiedzi "Last-Modified"

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

    last_modified = None
    current_last_modified = None

    for line in html_headers.splitlines():
        if line.startswith("Last-Modified:"):
            last_modified = line.split(":", 1)[1].strip()

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

        for line in html_headers.splitlines():
            if line.startswith("Last-Modified:"):
                current_last_modified = line.split(":", 1)[1].strip()

        if current_last_modified == last_modified:
            print("File hasn't changed, proceeding with download")
            image_data += html_body

            chunk_start = chunk_end + 1
            chunk_end += chunk_size
        else:
            print("The file has changed, aborting download")
            break

    if current_last_modified == last_modified:
        print("File hasn't changed, saving")
        with open("image.jpg", "wb") as f:
            f.write(image_data)
    else:
        print("The file has changed, it won't be saved")

except Exception as e:
    print(e)
