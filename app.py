from sanic import Sanic
from sanic.response import json
import threading, time, json, socket, sys, configparser
import routes

app = Sanic(strict_slashes=True)
routes.routes(app)

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

if __name__ == "__main__":
	# read pypatrol config
	#global config
	config = configparser.ConfigParser()
	config.read('pypatrol.conf')

	# populate pyPatrol-node settings
	node_name = config['node']['node_name']
	node_ip = config['node']['node_ip']
	node_port = int(config['node']['node_port'])
	bind_protocol = config['node']['bind_protocol']
	ipv4_capable = config.getboolean('node', 'ipv4_capable')
	ipv6_capable = config.getboolean('node', 'ipv6_capable')
	num_of_workers = int(config['node']['num_of_workers'])

	# populate pyPatrol-server settings
	server_host = config['server']['server_host']
	server_port = int(config['server']['server_port'])
	server_secret = config['server']['server_secret']
	standalone = config.getboolean('server', 'standalone')
	
	# populate SSL settings
	use_ssl = config.getboolean('ssl', 'use_ssl')
	ssl_cert = config['ssl']['ssl_cert']
	ssl_key = config['ssl']['ssl_key']
	ssl = {'cert': ssl_cert, 'key': ssl_key}

	if not standalone:
		d = threading.Thread(name='heartbeat', target=heartbeat)
        	d.setDaemon(True)
        	d.start()

	if (bind_protocol == "ipv6"):
		sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		sock.bind(('::', node_port))
		if use_ssl:
			app.run(sock=sock, workers=num_of_workers, ssl=ssl)
		else:
			app.run(sock=sock, workers=num_of_workers)
	elif (bind_protocol == "ipv4"):
		if use_ssl:
			app.run(host="0.0.0.0", port=node_port, workers=num_of_workers, ssl=ssl)
		else:
			app.run(host="0.0.0.0", port = node_port, workers=num_of_workers)
	else:
		print("Error parsing \"bind_protocol\". Please enter \'ipv4\' or \'ipv6\'.")
