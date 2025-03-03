import socket

ip_address = input()

try:
    hostname_info = socket.gethostbyaddr(ip_address)
    print(hostname_info[0])
except socket.error:
    print("No hostname found")
