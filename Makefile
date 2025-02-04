.PHONY: build upload test testcov testreport testreporthtml

build:
	py -m build

upload:
	twine upload --repository geolysis ./dist/*

test:
	pipenv run pytest

testcov:
	coverage run -m --rcfile=pyproject.toml pytest

testreport:
	coverage report

testreporthtml:
	coverage html
