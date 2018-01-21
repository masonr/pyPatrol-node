from sanic import Sanic
from sanic.response import json

import routes

app = Sanic()

routes.routes(app)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=43252, workers=10)
