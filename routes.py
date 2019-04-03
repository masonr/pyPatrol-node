from modules import *
from sanic_openapi import swagger_blueprint, openapi_blueprint, doc

def routes(app):

	### template ###
	#	@app.route("/mod_name")
	#	async def mod_name_req(request):
	#		return mod_name.invoke()
	###

	app.blueprint(openapi_blueprint)
	app.blueprint(swagger_blueprint)
	app.config.API_VERSION = '0.1'
	app.config.API_TITLE = 'pyPatrol API'
	app.config.API_DESCRIPTION = 'API Specification for pyPatrol Nodes'
	app.config.API_TERMS_OF_SERVICE = 'Use at own risk!'
	app.config.API_LICENSE_NAME = 'WTFPL License'
	app.config.API_LICENSE_URL = 'https://github.com/masonr/pyPatrol/blob/master/LICENSE'
	app.config.API_PRODUCES_CONTENT_TYPES = ['application/json']
	app.config.API_CONTACT_EMAIL = 'mason@rowe.sh'

	class Status:
		status = doc.String("Status of the service - {online/offline}")

	@app.route("/status")
	@doc.summary("Gets the status of the pyPatrol node")
	@doc.produces(Status)
	#@doc.responses(200, Status, description="pyPatrol node is online")
	async def status_req(request):
		return status.invoke()

	class Ping:
		ip = doc.String("IPv4 address or Hostname of machine")

	@app.route("/ping", methods=['POST'])
	@doc.summary("Pings (via IPv4) a specified IP/hostname")
	@doc.consumes(Ping, location="body")
	@doc.produces(Status)
	async def ping_req(request):
		return ping.invoke(request)

	class Ping6:
		ip = doc.String("IPv6 address or Hostname of machine")

	@app.route("/ping6", methods=['POST'])
	@doc.summary("Pings (via IPv6) a specified IP/hostname")
	@doc.consumes(Ping6, location="body")
	@doc.produces(Status)
	async def ping6_req(request):
		return ping6.invoke(request)

	class Cert:
		hostname = doc.String("Hostname of the website to check")
		buffer = doc.Integer("Number of days to start warning about soon to expire certs")

	class Cert_Status:
		valid = doc.String("Returns if the certificate is valid or not")
		reason = doc.String("Further explanation as to why the cert is valid or not")

	@app.route("/cert", methods=['POST'])
	@doc.summary("Checks if an SSL certificate is valid or will expire within a specified threshold")
	@doc.consumes(Cert, location="body")
	@doc.produces(Cert_Status)
	async def cert_req(request):
		return cert.invoke(request)

	class HTTP_Check:
		hostname = doc.String("URL or hostname of the website to check")
		redirects = doc.Boolean("Enables/disables the following of redirects (301/302)")
		check_string = doc.Boolean("Enables/disables searching for a specified text string on the page")
		keywords = doc.String("The string to search for if check_string is enabled")

	class HTTP_Status:
		status = doc.String("Status of the HTTP response - {online/offline}")
		code = doc.Integer("HTTP Response code")

	@app.route("/http_response", methods=['POST'])
	@doc.summary("Checks the HTTP response code of a given URL")
	@doc.consumes(HTTP_Check, location="body")
	@doc.produces(HTTP_Status)
	async def http_response_req(request):
		return http_response.invoke(request)

	class IP_Port_Check:
		ip = doc.String("IP address or Hostname of machine")
		port = doc.Integer("Port number to check on the host machine")

	@app.route("/tcp_socket", methods=['POST'])
	@doc.summary("Checks if a specified IP/hostname and port are listening for connections (TCP)")
	@doc.consumes(IP_Port_Check, location="body")
	@doc.produces(Status)
	async def tcp_socket_req(request):
		return tcp_socket.invoke(request)

	@app.route("/steam_server", methods=['POST'])
	@doc.summary("Checks if a Steam Server running on a specified IP/hostname and port is online")
	@doc.consumes(IP_Port_Check, location="body")
	@doc.produces(Status)
	async def steam_server_req(request):
		return steam_server.invoke(request)
