import socket

HOST = "127.0.0.1"
PORT = 1100

MESSAGES = {
    "Inbox": [
        {
            "body":
                "From: nadawca@interia.pl\r\n"
                "To: odbiorca@interia.pl\r\n"
                "Subject: Test1\r\n\r\n"
                "This is the first message.",

            "flags": ["\\Seen"]
        },
        {
            "body":
                "From: nadawca@interia.pl\r\n"
                "To: odbiorca@interia.pl\r\n"
                "Subject: Test2\r\n\r\n"
                "This is the second message.",

            "flags": []
        },
        {
            "body":
                "From: nadawca@interia.pl\r\n"
                "To: odbiorca@interia.pl\r\n"
                "Subject: Test3\r\n\r\n"
                "This is the third message.",

            "flags": []
        }
    ],

    "Inbox2": [
        {
            "body":
                "From: nadawca@interia.pl\r\n"
                "To: odbiorca@interia.pl\r\n"
                "Subject: Test3\r\n\r\n"
                "Very long message blah blah blah not really but you get the point.",

            "flags": ["\\Seen"]
        }
    ],

    "Drafts": [
        {
            "body":
                "From: nadawca@interia.pl\r\n"
                "To: \r\n"
                "Subject: \r\n\r\n"
                "",

            "flags": ["\\Draft", "\\Seen"]
        }
    ]
}

server_address = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

sock.listen(1)

print(f"IMAP server listening on {HOST}:{PORT}")

while True:
    client_socket, client_address = sock.accept()

    print(f"Connection from {client_address}")

    client_socket.sendall(b"* OK IMAP4 server ready\r\n")

    selected = None

    while True:
        data = client_socket.recv(1024)

        command = data.decode().strip()
        print(f"Received: {command}")

        parts = data.decode().replace("\r\n", "").split(' ')

        tag = parts[0]
        cmd = parts[1].upper()
        args = parts[2:]

        if cmd == "LOGIN":
            client_socket.sendall(f"{tag} OK Logged in\r\n".encode())

        elif cmd == "SELECT":
            mailbox = args[0]
            message_count = len(MESSAGES[mailbox])

            client_socket.sendall(f"* {message_count} EXISTS\r\n".encode())
            client_socket.sendall(f"* 0 RECENT\r\n".encode())
            client_socket.sendall(f"{tag} OK [READ-WRITE] SELECT completed\r\n".encode())

            selected = mailbox

        elif cmd == "LIST":
            for mailbox in MESSAGES:
                client_socket.sendall(f"* LIST (\\HasNoChildren) \"/\" \"{mailbox}\"\r\n".encode())

            client_socket.sendall(f"{tag} OK LIST completed\r\n".encode())

        elif cmd == "SEARCH":
            for arg in args:
                if not selected:
                    client_socket.sendall(f"{tag} BAD Please select a mailbox first\r\n".encode())
                    continue

                if arg.upper() == "UNSEEN":
                    unseen_messages = []
                    for i, mail in enumerate(MESSAGES[selected]):
                        if "\\Seen" not in mail["flags"]:
                            unseen_messages.append(str(i + 1))

                    client_socket.sendall(f"* Search {' '.join(unseen_messages)}\r\n".encode())

                elif arg.upper() == "DELETED":
                    marked_messages = []
                    for i, mail in enumerate(MESSAGES[selected]):
                        if "\\Deleted" in mail["flags"]:
                            marked_messages.append(str(i + 1))

                    client_socket.sendall(f"* Search {' '.join(marked_messages)}\r\n".encode())

            client_socket.sendall(f"{tag} OK Search completed\r\n".encode())

        elif cmd == "STORE":
            if not selected:
                client_socket.sendall(f"{tag} BAD Please select a mailbox first\r\n".encode())
                continue

            indices = []
            operator = None
            flags = []

            last_number = 0

            for i, arg in enumerate(args):
                if arg.isnumeric():
                    indices.append(int(arg) - 1)
                    last_number = i
                else:
                    break

            operator = args[last_number + 1]
            flags = ' '.join(args[last_number + 2:])

            flags = flags.replace("(", "").replace(")", "")
            flags = flags.split()

            for i, mail in enumerate(MESSAGES[selected]):
                if i in indices:
                    if operator.upper() == "+FLAGS":
                        for flag in flags:
                            mail["flags"].append(flag)
                    elif operator.upper() == "-FLAGS":
                        for flag in flags:
                            mail["flags"].remove(flags)

            client_socket.sendall(f"{tag} OK Store completed\r\n".encode())

        elif cmd == "FETCH":
            if not selected:
                client_socket.sendall(f"{tag} BAD Please select a mailbox first\r\n".encode())
                continue

            indices = []
            last_number = 0

            for i, arg in enumerate(args):
                if arg.isnumeric():
                    indices.append(int(arg) - 1)
                    last_number = i
                else:
                    break

            operator = args[last_number + 1]

            for index in indices:
                mail = MESSAGES[selected][index]
                size = len(mail["body"])

                if operator == "BODY[]":
                    client_socket.sendall(f"* {index + 1} FETCH (BODY[] {{{size}}}\r\n".encode())
                    client_socket.sendall(f"{mail["body"]}\r\n".encode())
                elif operator == "BODY[TEXT]":
                    message_body = mail["body"].splitlines()[4]

                    client_socket.sendall(f"* {index + 1} FETCH (BODY[TEXT] {{{size}}}\r\n".encode())
                    client_socket.sendall(f"{message_body}\r\n".encode())

            client_socket.sendall(f")\r\n{tag} OK Fetch completed\r\n".encode())

        elif cmd == "EXPUNGE":
            if not selected:
                client_socket.sendall(f"{tag} BAD Please select a mailbox first\r\n".encode())
                continue

            marked_messages = []

            for i, mail in enumerate(MESSAGES[selected]):
                if "\\Deleted" in mail["flags"]:
                    marked_messages.append((i, mail))

            for (i, mail) in marked_messages:
                MESSAGES[selected].remove(mail)
                client_socket.sendall(f"* {i + 1} EXPUNGE\r\n".encode())

            client_socket.sendall(f"{tag} OK Expunge completed\r\n".encode())

        elif cmd == "LOGOUT":
            client_socket.sendall(b"* BYE Logging out\r\n")
            client_socket.sendall(f"{tag} OK Logout completed\r\n".encode())
            break

        else:
            client_socket.sendall(f"{tag} BAD Unknown command \"{cmd}\"\r\n".encode())

    client_socket.close()
