import telnetlib
import base64
import re

HOST = "127.0.0.1"
PORT = 1100

MOCK_USERNAME = "student"
MOCK_PASSWORD = "123"


def send_command(command, timeout=5):
    print("C: ", command.strip().decode())
    tn.write(command)

    if command.decode().upper().startswith("RETR"):
        response = tn.read_until(b"\r\n.\r\n", timeout)
    else:
        response = tn.read_until(b"\r\n", timeout)

    print("S: ", response.decode())
    return response


tn = telnetlib.Telnet(HOST, PORT)

welcome = tn.read_until(b"\r\n", timeout=5)
print(welcome.decode().strip())

send_command(f"USER {MOCK_USERNAME}\r\n".encode())

send_command(f"PASS {MOCK_PASSWORD}\r\n".encode())

message = send_command(b"RETR 4\r\n").decode()

filename_match = re.search(r'filename="(.+?)"', message)
filename = filename_match.group(1) if filename_match else "attachment.bin"

base64_match = re.search(
    r'Content-Disposition: attachment; filename=".+?"\r\n\r\n(.+?)\r\n--',
    message,
    re.DOTALL
)

base64_data = base64_match.group(1).strip() if base64_match else None

if base64_data:
    with open(filename, "wb") as f:
        f.write(base64.b64decode(base64_data))
    print(f"Saved attachment as {filename}")
else:
    print("No base64 data found.")

tn.write(b"QUIT\r\n")
tn.close()
