.PHONY: build upload test testcov

build:
	py -m build

upload:
	twine upload --repository geolysis ./dist/*

test:
	pipenv run pytest

testcov:
	coverage run -m --rcfile=pyproject.toml pytest
	coverage report
