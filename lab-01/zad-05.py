import socket

hostname = input()

try:
    ip_address = socket.gethostbyname(hostname)
    print(ip_address)
except socket.error:
    print("No address found")
