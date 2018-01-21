import requests
from sanic.response import json, text

def check_website(hostname, redirects):
	try:
		req = requests.get(hostname, allow_redirects=redirects)
	except:
		return "offline", "404"	
	
	if str(req.status_code) == "200":
		return "online", "200"
	else:
		return "offline", str(req.status_code)

def invoke(request):
	hostname = request.json['hostname']
	redirects = request.json['redirects']
	if redirects == "true":
		redirects = True
	else:
		redirects = False
	status, code = check_website(hostname, redirects)
	return json({"status": status, "code": code})
