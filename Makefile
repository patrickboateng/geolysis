.PHONY: build upload test testcov testreport testreporthtml

PY_COMMAND  :=

# Check the operating system and set variables accordingly
ifeq ($(OS), Windows_NT)
    OS_NAME = Windows
    PY_COMMAND = py
else
 	UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S), Linux)
        PY_COMMAND = python3
    else ifeq ($(UNAME_S), Darwin)
		PY_COMMAND = python3
	else
		$(error Unsupported OS: $(UNAME_S))
	endif
endif

build:
	$(PY_COMMAND) -m build

upload:
	twine upload --repository geolysis ./dist/*

test:
	pipenv run pytest
	pipenv run $(PY_COMMAND) -m doctest README.md
	cd docs && make doctest
	
testcov:
	coverage run -m --rcfile=pyproject.toml pytest

testreport:
	coverage report

testreporthtml:
	coverage html
