import telnetlib

HOST = "127.0.0.1"
PORT = 1100

MOCK_USERNAME = "student"
MOCK_PASSWORD = "123"


def send_command(command, timeout=5):
    print("C:", command.strip().decode())
    tn.write(command)

    if command.decode().upper().startswith("RETR"):
        response = tn.read_until(b"\r\n.\r\n", timeout)
    else:
        response = tn.read_until(b"\r\n", timeout)

    print("S:", response.decode())
    return response


tn = telnetlib.Telnet(HOST, PORT)

welcome = tn.read_until(b"\r\n", timeout=5)
print(welcome.decode().strip())

send_command(f"USER {MOCK_USERNAME}\r\n".encode())

send_command(f"PASS {MOCK_PASSWORD}\r\n".encode())

message_list = send_command(b"LIST\r\n").decode().splitlines()

message_list.pop(0)
message_list.pop(len(message_list) - 1)

for message in message_list:
    split = message.split(' ')
    index = int(split[0])

    send_command(f"RETR {index}\r\n".encode())

send_command(b"QUIT\r\n")
tn.close()
