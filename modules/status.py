from sanic.response import json

def invoke():
	return json({"status": "online"})