import socket
import random
import string
import base64

HOST = "echo.websocket.events"
PORT = 80

RESOURCE = "/"

server_address = (HOST, PORT)

random_string = ''.join(random.choice(string.ascii_letters) for _ in range(16))
ws_key = base64.b64encode(random_string.encode()).decode()

print(random_string)
print(ws_key)

handshake = (
    f"GET {RESOURCE} HTTP/1.1\r\n"
    f"Host: {HOST}:{PORT}\r\n"
    "Upgrade: websocket\r\n"
    "Connection: Upgrade\r\n"
    f"Sec-WebSocket-Key: {ws_key}\r\n"
    "Origin: http://example.com\r\n"
    "Sec-WebSocket-Protocol: chat\r\n"
    "Sec-WebSocket-Version: 13\r\n\r\n"
)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
    print(f"Connected successfully to {HOST} at port {PORT}")

    sock.sendall(handshake.encode())

    data = sock.recv(4096).decode()
    print(f"Server response: {data}")

    message = "Hello chat".encode()

    frame = bytearray()
    frame.append(0x81)

    second_byte = 0x80 | len(message)
    frame.append(second_byte)

    mask = [random.randint(0, 255) for _ in range(4)]
    frame.extend(mask)

    masked_message = bytearray([message[i] ^ mask[i % 4] for i in range(len(message))])
    frame.extend(masked_message)

    sock.sendall(frame)

    response = sock.recv(4096)
    response_body = response[2:].decode()

    print(f"Server response: {response_body}")

except Exception as e:
    print(e)
