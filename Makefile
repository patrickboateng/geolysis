.PHONY: build upload test testcov testreport testreporthtml

build:
	py -m build

upload:
	twine upload --repository geolysis ./dist/*

test:
	pipenv run pytest
	cd docs && make doctest

testcov:
	coverage run -m --rcfile=pyproject.toml pytest

testreport:
	coverage report

testreporthtml:
	coverage html
