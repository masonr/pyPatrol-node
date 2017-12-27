import socket

def verifyIPv4(ip_addr):
	try:
		ip_addr = socket.gethostbyname(ip_addr)
		socket.inet_aton(ip_addr)
		print("Valid IPv4 Address: " + ip_addr)
		return ip_addr
	except socket.error:
		print("Invalid IPv4 Address: " + ip_addr)
		return None

def verifyIPv6(ip_addr):
	try:
		ip_addr = socket.getaddrinfo(ip_addr, None, socket.AF_INET6)[0][4][0]
		socket.inet_pton(socket.AF_INET6, ip_addr)
		print("Valid IPv6 Address: " + ip_addr)
		return ip_addr
	except socket.error:
		print("Invalid IPv6 Address: " + ip_addr)
		return None

def verifyHostname(hostname):
	try:
		socket.gethostbyname(hostname)
		print("Valid hostname: " + hostname)
		return True
	except socket.error:
		print("Invalid hostname: " + hostname)
		return False