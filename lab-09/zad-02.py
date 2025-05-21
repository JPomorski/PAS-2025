import socket

HOST = "httpbin.org"
PORT = 80

PATH = "/image/png"


def receive_all(sock):
    response = b""

    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break

        response += chunk

    return response


server_address = (HOST, PORT)

request = (
    f"GET {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Accept: image/png\r\n"
    "Connection: close\r\n\r\n"
)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    sock.sendall(request.encode())

    data = receive_all(sock)

    response_end = data.find(b"\r\n\r\n")
    print(f"Server response: {data[:response_end].decode()}")

    html_body = data[response_end + 4:]
    print(html_body)

    with open("image.png", "wb") as f:
        f.write(html_body)

except Exception as e:
    print(e)
