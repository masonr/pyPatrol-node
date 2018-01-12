import valve.source.a2s
from sanic.response import json, text
from utils import verifyIPv4

def check_server(host, port):
	host = verifyIPv4(host)
	if host is None or port > 65536 or port < 0:
		return "error"

	server_address = (host, port);
	try:
		with valve.source.a2s.ServerQuerier(server_address) as server:
			server.info();
			return "online";
	except:
		return "offline";


def invoke(request):
	host = request.json['ip']
	port = int(request.json['port'])
	print(host + " + : " + str(port))
	return json({"status": check_server(host, port)})