import socket
import base64
import hashlib

HOST = "127.0.0.1"
PORT = 80

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen(1)

print(f"WebSocket server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = sock.accept()

    print(f"Connection from {client_address}")

    try:
        request = client_socket.recv(1024).decode()
        print(request)

        request_lines = request.splitlines()

        key = None

        for line in request_lines:
            if line.startswith("Sec-WebSocket-Key:"):
                key = line.split(":")[1].strip()
                break

        if not key:
            client_socket.close()

        server_key = base64.b64encode(hashlib.sha1((key + GUID).encode()).digest()).decode()

        response = (
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {server_key}\r\n"
            f"Sec-WebSocket-Protocol: chat\r\n\r\n"
        )

        client_socket.send(response.encode())

        while True:
            message = client_socket.recv(4096)

            if not message:
                break

            second_byte = message[1]
            masked = second_byte >> 7
            message_length = second_byte & 0b01111111

            if message_length == 126:
                message_body = message[4:]
            elif message_length == 127:
                message_body = message[10:]
            else:
                message_body = message[2:]

            if masked:
                masking_key = message_body[:4]
                masked_body = message_body[4:]

                message_body = bytearray(masked_body[i] ^ masking_key[i % 4] for i in range(len(masked_body)))

            message_body = message_body.decode()
            print(message_body)

            frame = bytearray()
            frame.append(0x81)
            frame.append(0)

            response = (
                "Hello from WebSocket server sponsored by no one.\r\n"
                f"Received message: {message_body}"
            )

            frame.extend(response.encode())

            client_socket.sendall(frame)

    except Exception as e:
        print(e)

    finally:
        client_socket.close()
