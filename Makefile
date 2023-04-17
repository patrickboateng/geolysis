.PHONY: format test release

format:
	@isort src
	@isort tests
	@black src
	@black tests

test:
	@echo "Running pytest..."
	@pytest
	@echo "Running doctest..."
	@py -m doctest README.md
	@echo "All tests passed"

release:
	@xlwings release