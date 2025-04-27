import socket

HOST = "127.0.0.1"
PORT = 1100


def send_command(command):
    print("C:", command.strip())
    sock.sendall(command.encode())

    response = b""

    while True:
        response += sock.recv(1024)
        split = response.decode().split('\r\n')
        split.pop()

        if not split[len(split) - 1].startswith("*"):
            break

    print("S:", response.decode())
    return response


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

sock.recv(1024)

send_command("A1 LOGIN student 123\r\n")

send_command("A2 SELECT Inbox\r\n")

send_command("A3 SEARCH DELETED\r\n")

send_command(f"A4 STORE 1 2 +FLAGS \\Deleted\r\n")

send_command("A5 SEARCH DELETED\r\n")

send_command(f"A6 EXPUNGE\r\n")

send_command("A7 SEARCH DELETED\r\n")

send_command("A8 SELECT Inbox\r\n")

send_command("A9 LOGOUT\r\n")

sock.close()
