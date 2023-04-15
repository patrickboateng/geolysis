.PHONY: test release

test:
	@echo "Running pytest..."
	@pytest
	@echo "Running doctest..."
	@py -m doctest README.md
	@echo "All tests passed"

release:
	@xlwings release