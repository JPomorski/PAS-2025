import socket
import base64

HOST = "127.0.0.1"
PORT = 1100

USERNAME = "nadawca@interia.pl"
PASSWORD = ""

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen(1)

print(f"SMTP server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = sock.accept()
    print(f"Connection from {client_address}")

    client_socket.send(b"220 SMTP Localhost\r\n")

    username_provided = False
    password_provided = False
    temp_username = ""

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        command = data.decode('utf-8').strip()
        print(f"C: {command}")

        if command.startswith("EHLO") or command.startswith("HELO"):
            client_socket.send(b"250-Hello\r\n250-AUTH LOGIN\r\n250 OK\r\n")

        elif command == "AUTH LOGIN":
            client_socket.send(b"334 VXNlcm5hbWU6\r\n")

        elif not username_provided:
            try:
                temp_username = base64.b64decode(command).decode('utf-8')
                client_socket.send(b"334 UGFzc3dvcmQ6\r\n")
                username_provided = True

            except Exception as e:
                client_socket.send(b"500 Invalid base64 for username\r\n")
                username_provided = False
                print(e)

        elif not password_provided:
            try:
                temp_password = base64.b64decode(command).decode('utf-8')

                if temp_username == USERNAME and temp_password == PASSWORD:
                    client_socket.send(b"235 Authentication successful\r\n")
                    password_provided = True
                else:
                    client_socket.send(b"535 Authentication credentials invalid\r\n")
                    username_provided = False
                    password_provided = False

            except Exception as e:
                client_socket.send(b"500 Invalid base64 for password\r\n")
                password_provided = False
                print(e)

        elif command.startswith("MAIL FROM:"):
            client_socket.send(b"250 OK\r\n")

        elif command.startswith("RCPT TO:"):
            client_socket.send(b"250 OK\r\n")

        elif command == "DATA":
            client_socket.send(b"354 End data with <CRLF>.<CRLF>\r\n")
            message_data = client_socket.recv(1024).decode('utf-8')

            print("Received email:")
            print(message_data)
            client_socket.send(b"250 OK\r\n")

        elif command == "QUIT":
            client_socket.send(b"221 Bye\r\n")
            break

        else:
            client_socket.send(b"502 Error: command not recognized\r\n")

    client_socket.close()
