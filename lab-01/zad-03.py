import ipaddress

ip_address = input("Enter IP address: ")

try:
    ipaddress.ip_address(ip_address)
    print("The given address is ok")
except ValueError:
    print("The given address is invalid")
