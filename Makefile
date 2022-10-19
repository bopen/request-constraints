.DEFAULT_GOAL := open

api_server:
	tranquilizer restapi.py --allow-origin "*"

web_app:
	cd webapp && python -m http.server 8085

open:
	open http://localhost:8085

all: api_server web_app open