import base64
import telnetlib
import time

HOST = "smtp.interia.pl"
PORT = 587

USERNAME = "_"
PASSWORD = "_"

MAIL_FROM = "_"
RCPT_TO = "_"
SUBJECT = "Testowa wiadomość ESMTP :333"
BODY = ":33333"


def send_command(tn, command, wait=1):
    tn.write(command.encode('utf-8'))
    time.sleep(wait)
    response = tn.read_very_eager().decode('utf-8')
    return response


tn = telnetlib.Telnet(HOST, PORT)

print("Banner:", tn.read_until(b"\n").decode('utf-8'))

send_command(tn, "EHLO localhost\r\n")

# send_command(tn, "STARTTLS\r\n")

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
send_command(tn, message, wait=2)

# send_command(tn, "QUIT\r\n")

tn.close()
