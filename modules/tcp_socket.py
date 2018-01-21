import socket
from contextlib import closing
from sanic.response import json, text
from utils import verifyIPv4

def check_socket(host, port):
	host = verifyIPv4(host)
	if host is None or port > 65536 or port < 0:
		return "error"

	with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
		sock.settimeout(3)
		if sock.connect_ex((host, port)) == 0:
			return "online"
		else:
			return "offline"

def invoke(request):
	host = request.json['ip']
	port = int(request.json['port'])
	return json({"status": check_socket(host, port)})