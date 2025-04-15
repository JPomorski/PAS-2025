import socket
import base64

HOST = "127.0.0.1"
PORT = 1100

MOCK_USERNAME = "student"
MOCK_PASSWORD = "123"

with open("../lab-06/brainrot.png", "rb") as f:
    file_data = f.read()
    encoded_file = base64.b64encode(file_data).decode('utf-8')

MESSAGES = [
    "From: nadawca@interia.pl\r\n"
    "To: odbiorca@interia.pl\r\n"
    "Subject: Test1\r\n\r\n"
    "This is the first message.",

    "From: nadawca@interia.pl\r\n"
    "To: odbiorca@interia.pl\r\n"
    "Subject: Test2\r\n\r\n"
    "This is the second message.",

    "From: nadawca@interia.pl\r\n"
    "To: odbiorca@interia.pl\r\n"
    "Subject: Test3\r\n\r\n"
    "Very long message blah blah blah not really but you get the point.",

    "From: nadawca@interia.pl\r\n"
    "To: odbiorca@interia.pl\r\n"
    "Subject: Test4\r\n"
    "MIME-Version: 1.0\r\n"
    "Content-Type: multipart/mixed; boundary=test4\r\n"
    "\r\n"
    "--test4\r\n"
    "Content-Type: text/plain; charset=\"utf-8\"\r\n"
    "Content-Transfer-Encoding: 7bit\r\n"
    "\r\n"
    "Tralalero tralala\r\n"
    "\r\n"
    "--test4\r\n"
    "Content-Type: image/png; name=\"image.png\"\r\n"
    "Content-Transfer-Encoding: base64\r\n"
    "Content-Disposition: attachment; filename=\"image.png\"\r\n"
    "\r\n"
    f"{encoded_file}\r\n"
    "--test4--\r\n"
]

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen(1)

print(f"POP3 Server listening on {HOST}:{PORT}")


while True:
    client_socket, client_address = sock.accept()

    print(f"Connection from {client_address}")

    client_socket.sendall(b"+OK Mock POP3 Server Ready\r\n")

    authorized = False

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        command = data.decode().strip()
        print(f"Received: {command}")

        if command.upper().startswith("USER"):
            if MOCK_USERNAME in command:
                client_socket.sendall(b"+OK Tell me your password.\r\n")
            else:
                client_socket.sendall(b"-ERR Invalid user\r\n")

        elif command.upper().startswith("PASS"):
            if MOCK_PASSWORD in command:
                authorized = True
                num_msgs = len(MESSAGES)
                client_socket.sendall(f"+OK Welcome aboard! You have {num_msgs} messages.\r\n".encode())
            else:
                client_socket.sendall(b"-ERR Invalid password\r\n")

        elif command.upper() == "STAT":
            if authorized:
                num_msgs = len(MESSAGES)
                total_size = sum(len(m.encode()) for m in MESSAGES)
                client_socket.sendall(f"+OK {num_msgs} {total_size}\r\n".encode())
            else:
                client_socket.sendall(b"-ERR Not authenticated\r\n")

        elif command.upper() == "LIST":
            if authorized:
                message_list = "+OK Scan list follows:\n"

                for i, msg in enumerate(MESSAGES):
                    message_list += f"{i+1} {len(msg.encode())}\n"

                message_list += ".\r\n"
                client_socket.sendall(message_list.encode())
            else:
                client_socket.sendall(b"-ERR Not authorized\r\n")

        elif command.upper().startswith("RETR"):
            parts = command.split()

            if len(parts) != 2:
                client_socket.sendall(b"-ERR Usage: RETR <index>\r\n")
                continue

            try:
                msg_index = int(parts[1]) - 1

                if 0 <= msg_index < len(MESSAGES):
                    message = MESSAGES[msg_index]
                    response = "+OK Message follows\r\n"

                    for line in message.splitlines():
                        if line.startswith("."):
                            line = "." + line
                        print(line)
                        response += f"{line}\r\n"

                    response += ".\r\n"
                    client_socket.sendall(response.encode())
                else:
                    client_socket.sendall(b"-ERR No such message\r\n")

            except ValueError:
                client_socket.sendall(b"-ERR Invalid message number\r\n")

        elif command.upper().startswith("DELE"):
            parts = command.split()

            if len(parts) != 2:
                client_socket.sendall(b"-ERR Usage: DELE <index>\r\n")
                continue

            try:
                msg_index = int(parts[1]) - 1

                if 0 <= msg_index < len(MESSAGES):
                    MESSAGES.pop(msg_index)
                    response = f"+OK Message {parts[1]} deleted\r\n"
                    response += "Current inbox state:\r\n"

                    for i, msg in enumerate(MESSAGES):
                        response += f"{i + 1} {len(msg.encode())}\n"

                    response += ".\r\n"
                    client_socket.sendall(response.encode())
                else:
                    client_socket.sendall(b"-ERR No such message\r\n")

            except ValueError:
                client_socket.sendall(b"-ERR Invalid message number\r\n")

        elif command.upper() == "QUIT":
            client_socket.sendall(b"+OK Goodbye\r\n")
            break

        else:
            client_socket.sendall(b"-ERR Unknown command\r\n")

    client_socket.close()
