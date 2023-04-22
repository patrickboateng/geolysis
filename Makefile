.PHONY: format test release

format:
	@isort src
	@isort tests
	@black src
	@black tests
	# @docformatter -i src

test:
	@echo "Running pytest..."
	@pytest
	@echo "Running doctest..."
	@py -m doctest README.md
	@py -m doctest docs/index.md
	@echo "All tests passed"

release:
	@xlwings release