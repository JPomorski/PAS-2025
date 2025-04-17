import telnetlib

HOST = "127.0.0.1"
PORT = 1100

MOCK_USERNAME = "student"
MOCK_PASSWORD = "123"


def send_command(command, timeout=5):
    print("C:", command.strip().decode())
    tn.write(command)
    response = tn.read_until(b".\r\n", timeout)
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

min_split = message_list[0].split(' ')
min_size = int(min_split[1])
min_index = int(min_split[0])

for message in message_list:
    split = message.split(' ')
    size = int(split[1])
    index = int(split[0])

    if size < min_size:
        min_size = size
        min_index = index

send_command(f"DELE {min_index}\r\n".encode())

send_command(b"QUIT\r\n")
tn.close()
