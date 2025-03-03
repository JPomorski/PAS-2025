import ipaddress

ip_address = input()

try:
    ipaddress.ip_address(ip_address)
except ValueError:
    print("The given address is invalid")
