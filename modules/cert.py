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
		return "invalid", "expired"
	except socket.timeout: # timeout connecting to host
		conn.close()
		return "error", "timeout"
	except: # other error
		conn.close()
		return "error", "error"

	cert = conn.getpeercert()
	conn.close()
	valid_until = datetime.datetime.strptime(cert['notAfter'], r'%b %d %H:%M:%S %Y %Z')
	days_left = valid_until - datetime.datetime.utcnow()

	if days_left < datetime.timedelta(days=0):
		# Cert is expired
		return "invalid", "expired"
	elif days_left < datetime.timedelta(days=int(buffer_days)):
		# Cert expires in days buffer range
		return "valid", "expires soon"
	else:
		# Cert is valid
		return "valid", "valid"


def invoke(request):
	hostname = request.json['hostname']
	buffer_days = request.json['buffer']
	valid_res, reason = check_cert(hostname, buffer_days)
	return json({"status": valid_res, "reason": reason})
