import socket

HOST = "httpbin.org"
PORT = 80

PATH = "/post"


def receive_all(sock):
    response = b""

    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break

        response += chunk

    return response


server_address = (HOST, PORT)

form_data = {
    "name": "Jan",
    "email": "jan@example.com"
}

url_data = '&'.join(f"{field}={value}" for field, value in form_data.items())

request = (
    f"POST {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Content-Type: application/x-www-form-urlencoded\r\n"
    f"Content-Length: {len(url_data)}\r\n"
    "Connection: close\r\n\r\n"
    f"{url_data}"
)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    sock.sendall(request.encode())

    data = receive_all(sock)

    response_end = data.find(b"\r\n\r\n")
    print(f"Server response: {data[:response_end].decode()}")

except Exception as e:
    print(e)
