PROJECT := cads_catalogue_api_service
CONDA := conda
CONDAFLAGS :=
COV_REPORT := html
.DEFAULT_GOAL := main


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

main:
	uvicorn --host 0.0.0.0 --port 8086 restapi:app --reload 

open:
	open http://localhost:8086

