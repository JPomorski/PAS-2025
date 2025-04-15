import base64
import telnetlib
import time

HOST = "smtp.interia.pl"
PORT = 587

USERNAME = "nadawca@interia.pl"
PASSWORD = ""

MAIL_FROM = "nadawca@interia.pl"
RCPT_TO = "odbiorca@interia.pl"
SUBJECT = "Wiadomość sformatowana za pomocą HTML"
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
    f"MIME-Version: 1.0\r\n"
    f"Content-Type: text/html; charset=UTF-8\r\n"
    "\r\n"
    f"<html>\r\n"
    f"<body>\r\n"
    f"<h1>Nagłówek</h1>\r\n"
    f"<p>{BODY}</p>\r\n"
    f"<p>Zwykły tekst</p>\r\n"
    f"<p><b>Pogrubiony tekst</b></p>\r\n"
    f"<p><i>Kursywa</i></p>\r\n"
    f"<p><a href='https://www.python.org'>Link</a>.</p>\r\n"
    f"</body>\r\n"
    f"</html>\r\n"
    ".\r\n"
)

mock_send_command(message)

send_command(tn, "QUIT\r\n")

tn.close()
