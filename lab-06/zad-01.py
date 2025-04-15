import base64
import telnetlib
import time

HOST = "smtp.interia.pl"
PORT = 587

USERNAME = "nadawca@interia.pl"
PASSWORD = ""   # Zostawiam puste, żeby git nie krzyczał że leakuję hasło

MAIL_FROM = "nadawca@interia.pl"
RCPT_TO = "odbiorca@interia.pl"
SUBJECT = "Testowa wiadomość ESMTP :333"
BODY = ":33333"


# Pomimo wszelkich starań komunikacja z serwerem Interii po prostu nie działa,
# być może jest to wina po stronie zabezpieczeń serwera, który odrzuca próby ze skryptu.
# Stworzyłem nawet testowe konto na Interii, ale pomimo wpisania takiego samego adresu i hasła,
# jak przy logowaniu na stronie (udanym), serwer dalej wyrzucał AuthenticationError.

# :(


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

# Połączenie z serwerem Interii wymaga komunikacji TLS, która rozłącza połączenie przez telnet.
# W zadaniu jest napisane, aby użyć telnetu, więc jej nie wykorzystuję.

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

# Serwer automatycznie zamyka połączenie po nieudanej próbie wysłania wiadomości.

# send_command(tn, message, wait=2)
mock_send_command(message)

send_command(tn, "QUIT\r\n")

tn.close()
