.PHONY: build upload rc run

build:
	py -m build

upload:
	twine upload --repository geolysis ./dist/*

RESOURCE_PATH := ./geolysis/ui/assets

rc:
	pyside6-rcc $(RESOURCE_PATH)/resources.qrc -o $(RESOURCE_PATH)/resources_rc.py

OS_NAME :=
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

run:
	$(PY_COMMAND) ./geolysis/ui/main.py
