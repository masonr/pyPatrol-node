import os
from sanic.response import json, text
from utils import verifyIPv4

def ping(ip_addr):
	ip_addr = verifyIPv4(ip_addr)
	if ip_addr is None:
		return "error"

	response = os.system("ping -c 1 -w2 " + ip_addr + " > /dev/null 2>&1")
	if response == 0:
	  status = "online"
	else:
	  status = "offline"

	return status

def invoke(request):
	ip_addr = request.json['ip']
	print(ip_addr)
	return json({"status": ping(ip_addr)})