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

mailbox_list = send_command("A2 LIST\r\n")

mailboxes = []

mailbox_list = mailbox_list.decode().strip().splitlines()
mailbox_list.pop(len(mailbox_list) - 1)

for mailbox in mailbox_list:
    mailboxes.append(mailbox.split(' ')[4].replace("\"", ""))

message_count = 0

for mailbox in mailboxes:
    inbox_state = send_command(f"A3 SELECT {mailbox}\r\n")

    for line in inbox_state.decode().splitlines():
        if line.startswith('*') and 'EXISTS' in line:
            message_count += int(line.split()[1])
            break

print(f"Message count in all mailboxes: {message_count}\r\n")

send_command("A4 LOGOUT\r\n")

sock.close()
