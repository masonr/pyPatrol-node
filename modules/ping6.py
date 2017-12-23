import os
from sanic.response import json
from utils import verifyIPv6

def ping6():
	hostname = "2607:f8b0:4004:805::200e" #example
	verifyIPv6(hostname)
	response = os.system("ping6 -c 1 -w2 " + hostname + " > /dev/null 2>&1")

	#and then check the response...
	if response == 0:
	  status = "online"
	else:
	  status = "offline"

	return status

def invoke():
	return json({"status": ping6()})