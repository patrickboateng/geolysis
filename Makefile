.PHONY: build upload

build:
	py -m build

upload:
	twine upload --repository geolysis ./dist/*
