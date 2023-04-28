.PHONY: format test release check

check:
	@mypy geolab
	@pycodestyle --statistics geolab

format:
	@isort ./geolab
	@isort ./soil_classifier_addin.py
	@isort ./tests
	@black ./geolab
	@black ./tests
	@docformatter -i ./geolab

test:
	@echo "Running pytest..."
	@pytest
	@echo "Running doctest..."
	@py -m doctest README.md
	@py -m doctest docs/index.md
	@echo "All tests passed"

release:
	@xlwings release