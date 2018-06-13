import requests
from sanic.response import json, text

def check_website(hostname, redirects, check_string, keywords):
	try:
		req = requests.get(hostname, allow_redirects=redirects)
	except:
		return "offline", "404"	
	
	if str(req.status_code) == "200":
		if (check_string):
			if keywords not in req.text:
				return "offline", "200"
			else:
				return "online", "200"
		else:
			return "online", "200"
	else:
		return "offline", str(req.status_code)

def invoke(request):
	hostname = request.json['hostname']
	redirects = request.json['redirects']
	check_string = request.json['check_string']
	keywords = request.json['keywords']
	if redirects == "true":
		redirects = True
	else:
		redirects = False
	if check_string == "true":
		check_string = True
	else:
		check_string = False
	status, code = check_website(hostname, redirects, check_string, keywords)
	return json({"status": status, "code": code})
