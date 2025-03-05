import socket

ip_address = input("Enter IP address: ")

try:
    hostname_info = socket.gethostbyaddr(ip_address)
    print(hostname_info[0])
except socket.error:
    print("No hostname found")
