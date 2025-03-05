import socket

hostname = input("Enter hostname: ")

try:
    ip_address = socket.gethostbyname(hostname)
    print(ip_address)
except socket.error:
    print("No address found")
