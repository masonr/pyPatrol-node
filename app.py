from sanic import Sanic
from sanic.response import json
import threading, requests, time, json
import routes

app = Sanic()
routes.routes(app)

# config vars
node_ip="127.0.0.1"				# ip or hostname of the pyPatrol node
node_port=12345					# port of the pyPatrol node
mothership_host="127.0.0.1"		# ip or hostname of the pyMothership server
mothership_port=12346			# port of the pyMothership server
ipv4_capable=True				# pyPatrol node ipv4 capable?
ipv6_capable=True				# pyPatrol node ipv6 capable?
standalone=False				# standalone mode or connect to pyMothership server
num_of_workers=10				# number of async workers

def heartbeat():
	uri = 'http://' + mothership_host + ':' + str(mothership_port)
	data = {'ipv4': ipv4_capable,
			'ipv6': ipv6_capable
			}
	headers = {'content-type': 'application/json'}

	while (True):
		requests.post(uri, data=json.dumps(data), headers=headers)
		time.sleep(30) # sleep for 30s

if (not standalone):
	d = threading.Thread(name='heartbeat', target=heartbeat)
	d.setDaemon(True)
	d.start()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=node_port, workers=num_of_workers)
