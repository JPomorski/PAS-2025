import socket

HOST = "httpbin.org"
PORT = 80

PATH = "/html"


def receive_all(sock):
    response = b""

    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break

        response += chunk

    return response.decode()


server_address = (HOST, PORT)

request = (
    f"GET {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14"
    " (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A\r\n"
    "Connection: close\r\n\r\n"
)

# Do podszycia się pod przeglądarkę Safari (oprócz GET i Host) potrzebny jest nagłówek "User-Agent".
# Część z podanych w nim informacji jest opcjonalna, ale zazwyczaj z punktu widzenia serwera
# im bardziej dokładne te informacje, tym bardziej "prawdziwie" wygląda ten nagłówek

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    sock.sendall(request.encode())

    data = receive_all(sock)
    print(f"Server response: {data}")

    response_end = data.find("\r\n\r\n")
    html_body = data[response_end + 4:]

    with open("index.html", "wb") as f:
        f.write(html_body.encode())

except Exception as e:
    print(e)
