import datetime
import socket
import ssl
from sanic.response import json, text

def check_cert(hostname, buffer_days):
	context = ssl.create_default_context()
	conn = context.wrap_socket(
		socket.socket(socket.AF_INET),
		server_hostname=hostname,
	)

	conn.settimeout(3.0)

	try:
		conn.connect((hostname, 443))
	except ssl.SSLError: # expired or misconfigured
		conn.close()
		return "false", "expired"
	except socket.timeout: # timeout connecting to host
		conn.close()
		return "false", "timeout"
	except: # other error
		conn.close()
		return "false", "error"

	cert = conn.getpeercert()
	conn.close()
	valid_until = datetime.datetime.strptime(cert['notAfter'], r'%b %d %H:%M:%S %Y %Z')
	days_left = valid_until - datetime.datetime.utcnow()

	if days_left < datetime.timedelta(days=0):
		# Cert is expired
		return "false", "expired"
	elif days_left < datetime.timedelta(days=int(buffer_days)):
		# Cert expires in days buffer range
		return "true", "expires soon"
	else:
		# Cert is valid
		return "true", "valid"


def invoke(request):
	hostname = request.json['hostname']
	buffer_days = request.json['buffer']
	valid_res, reason = check_cert(hostname, buffer_days)
	return json({"valid": valid_res, "reason": reason})