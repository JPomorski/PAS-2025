import base64
import telnetlib
import time

HOST = "smtp.interia.pl"
PORT = 587

USERNAME = "nadawca@interia.pl"
PASSWORD = ""

MAIL_FROM = "prezydent@interia.pl"
RCPT_TO = "odbiorca@interia.pl"
SUBJECT = "Wiadomość od pwezydenta >w< [100% LEGIT]"
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
    "\r\n"
    f"{BODY}\r\n"
    ".\r\n"
)

mock_send_command(message)

send_command(tn, "QUIT\r\n")

tn.close()
