from modules import *

def routes(app):

	### template ###
	#	@app.route("/mod_name")
	#	async def mod_name_req(request):
	#		return mod_name.invoke()
	###

	@app.route("/status")
	async def status_req(request):
		return status.invoke()

	@app.route("/ping", methods=['POST'])
	async def ping_req(request):
		return ping.invoke(request)

	@app.route("/ping6", methods=['POST'])
	async def ping6_req(request):
		return ping6.invoke(request)

	@app.route("/cert", methods=['POST'])
	async def cert_req(request):
		return cert.invoke(request)

	@app.route("/http_response", methods=['POST'])
	async def http_response_req(request):
		return http_response.invoke(request)

