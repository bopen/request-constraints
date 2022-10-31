PROJECT := cads_catalogue_api_service
CONDA := conda
CONDAFLAGS :=
COV_REPORT := html
.DEFAULT_GOAL := open


default: qa unit-tests type-check

qa:
	pre-commit run --all-files

unit-tests:
	python -m pytest -vv --cov=. --cov-report=$(COV_REPORT)

type-check:
	python -m mypy --strict .

conda-env-update:
	$(CONDA) env update $(CONDAFLAGS) -f environment.yml

template-update:
	pre-commit run --all-files cruft -c .pre-commit-config-weekly.yaml

docs-build:
	cd docs && rm -fr _api && make clean && make html

# DO NOT EDIT ABOVE THIS LINE, ADD COMMANDS BELOW

api_server:
	tranquilizer restapi.py --allow-origin "*"

web_app:
	cd webapp && python -m http.server 8085

open:
	open http://localhost:8085

all: api_server web_app open
