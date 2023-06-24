.PHONY: check format test

check:
	@mypy geolab
	@pycodestyle --statistics geolab

format:
	@isort ./geolab
	@isort ./tests
	@black ./geolab
	@black ./tests

test:
	@echo "Running pytest..."
	@pytest
