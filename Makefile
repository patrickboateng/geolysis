.PHONY: check format test build upload

check:
	@mypy geolysis
	@pycodestyle --statistics geolysis

format:
	@isort ./geolysis
	@isort ./tests
	@black ./geolysis
	@black ./tests

test:
	@echo "Running pytest..."
	pytest

build:
	py -m build

upload:
	twine upload --repository geolysis ./dist/*