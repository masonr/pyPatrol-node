from sanic import Sanic
from sanic.response import json
import threading, time, json, socket, sys
import routes

app = Sanic(strict_slashes=True)
routes.routes(app)

# config vars
node_name="PYPATROL_NODE1"		# descriptor of the pyPatrol node
node_ip="127.0.0.1"				# ip or hostname of the pyPatrol node
node_port=12345					# port of the pyPatrol node
server_host="127.0.0.1"			# ip or hostname of the pyPatrol server
server_port=12355				# port of the pyPatrol server
server_secret="secret"			# secret keyword for auth to pyPatrol server
ipv4_capable=True				# pyPatrol node ipv4 capable?
ipv6_capable=True				# pyPatrol node ipv6 capable?
standalone=False				# standalone mode or connect to pyPatrol server
num_of_workers=10				# number of async workers
use_ssl=False					# set if SSL (HTTPS) connections should be utilized
if use_ssl:						# fill in SSL certificate information if use_ssl is True
	ssl = {'cert': "/path/to/cert", 'key': "/path/to/keyfile"}

def heartbeat():
	data = {
			'name': node_name,
			'ip': node_ip,
			'port': node_port,
			'ipv4': ipv4_capable,
			'ipv6': ipv6_capable,
			'ssl': use_ssl,
			'secret': server_secret
			}

	while True:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((server_host, server_port))
			sock.send(json.dumps(data).encode())
		except:
			print('Unable to establish connection to the server. Sleeping...')
		finally:
			sock.close()
		time.sleep(30) # sleep for 30s

if not standalone:
	d = threading.Thread(name='heartbeat', target=heartbeat)
	d.setDaemon(True)
	d.start()

if __name__ == "__main__":
	if use_ssl:
		app.run(host="0.0.0.0", port=node_port, workers=num_of_workers, ssl=ssl)
	else:
		app.run(host="0.0.0.0", port=node_port, workers=num_of_workers)
