import telnetlib

HOST = "127.0.0.1"
PORT = 1100

MOCK_USERNAME = "student"
MOCK_PASSWORD = "123"


def send_command(command, timeout=5):
    print("C:", command.strip().decode())
    tn.write(command)
    response = tn.read_until(b"\r\n", timeout)
    print("S:", response.decode())
    return response


tn = telnetlib.Telnet(HOST, PORT)

welcome = tn.read_until(b"\r\n", timeout=5)
print(welcome.decode().strip())

send_command(f"USER {MOCK_USERNAME}\r\n".encode())

send_command(f"PASS {MOCK_PASSWORD}\r\n".encode())

send_command(b"LIST\r\n")

send_command(b"QUIT\r\n")
tn.close()
