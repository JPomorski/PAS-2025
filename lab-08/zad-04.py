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


def send_using_tag(tag, command):
    print("C:", command.strip())
    sock.sendall(command.encode())

    response = b""

    while True:
        response += sock.recv(1024)
        split = response.decode().split('\r\n')
        split.pop()

        if split[len(split) - 1].startswith(tag):
            break

    print("S:", response.decode())
    return response


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

sock.recv(1024)

send_command("A1 LOGIN student 123\r\n")

send_command("A2 SELECT Inbox\r\n")

unseen_messages = send_command("A3 SEARCH UNSEEN\r\n")

unseen_messages = unseen_messages.decode().splitlines()[0].split(' ')
unseen_indices = unseen_messages[2:]

send_using_tag("A4", f"A4 FETCH {' '.join(unseen_indices)} BODY[]\r\n")

send_command(f"A5 STORE {' '.join(unseen_indices)} +FLAGS (\\Seen)\r\n")

send_command("A6 SEARCH UNSEEN\r\n")

send_command("A7 LOGOUT\r\n")

sock.close()
