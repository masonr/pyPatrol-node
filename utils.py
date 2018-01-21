import socket

def verifyIPv4(ip_addr):
	try:
		ip_addr = socket.gethostbyname(ip_addr)
		socket.inet_aton(ip_addr)
		# Valid IPv4 Address
		return ip_addr
	except socket.error:
		# Invalid IPv4 Address
		return None

def verifyIPv6(ip_addr):
	try:
		ip_addr = socket.getaddrinfo(ip_addr, None, socket.AF_INET6)[0][4][0]
		socket.inet_pton(socket.AF_INET6, ip_addr)
		#Valid IPv6 Address
		return ip_addr
	except socket.error:
		# Invalid IPv6 Address
		return None

def verifyHostname(hostname):
	try:
		socket.gethostbyname(hostname)
		# Valid hostname
		return True
	except socket.error:
		# Invalid hostname
		return False