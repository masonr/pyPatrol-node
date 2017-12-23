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

	@app.route("/ping6")
	async def ping6_req(request):
		return ping6.invoke()

	@app.route("/cert")
	async def cert_req(request):
		return cert.invoke("todo")