import base64
import telnetlib
import time

HOST = "smtp.interia.pl"
PORT = 587

USERNAME = "nadawca@interia.pl"
PASSWORD = ""

MAIL_FROM = "nadawca@interia.pl"
RCPT_TO = "odbiorca@interia.pl"
SUBJECT = "Wiadomość z plikiem tekstowym"
BODY = ":33333"


def send_command(tn, command, wait=1):
    print("C:", command.strip())
    tn.write(command.encode('utf-8'))
    time.sleep(wait)
    response = tn.read_very_eager().decode('utf-8')
    print("S:", response)
    return response


def mock_send_command(command, wait=1):
    print("C:", command.strip())
    time.sleep(wait)
    print("S: 250 OK\r\n")


with open("plik.txt", "rb") as f:
    file_data = f.read()
    encoded_file = base64.b64encode(file_data).decode('utf-8')

boundary = "alamakota"

tn = telnetlib.Telnet(HOST, PORT)

print("Banner:", tn.read_until(b"\n").decode('utf-8'))

send_command(tn, "EHLO localhost\r\n")

send_command(tn, "AUTH LOGIN\r\n")

username_b64 = base64.b64encode(USERNAME.encode('utf-8')).decode('utf-8')
send_command(tn, username_b64 + "\r\n")

password_b64 = base64.b64encode(PASSWORD.encode('utf-8')).decode('utf-8')
send_command(tn, password_b64 + "\r\n")

send_command(tn, f"MAIL FROM:<{MAIL_FROM}>\r\n")

send_command(tn, f"RCPT TO:<{RCPT_TO}>\r\n")

send_command(tn, "DATA\r\n")

message = (
    f"From: {MAIL_FROM}\r\n"
    f"To: {RCPT_TO}\r\n"
    f"Subject: {SUBJECT}\r\n"
    f"MIME-Version: 1.0\r\n"
    f"Content-Type: multipart/mixed; boundary={boundary}\r\n"
    "\r\n"
    f"--{boundary}\r\n"
    "Content-Type: text/plain; charset=\"utf-8\"\r\n"
    "Content-Transfer-Encoding: 7bit\r\n"
    "\r\n"
    f"{BODY}\r\n"
    "\r\n"
    f"--{boundary}\r\n"
    "Content-Type: text/plain; name=\"plik.txt\"\r\n"
    "Content-Transfer-Encoding: base64\r\n"
    "Content-Disposition: attachment; filename=\"plik.txt\"\r\n"
    "\r\n"
    f"{encoded_file}\r\n"
    f"--{boundary}--\r\n"
    ".\r\n"
)

mock_send_command(message)

send_command(tn, "QUIT\r\n")

tn.close()
