.PHONY: build upload

build:
	py -m build

upload:
	twine upload --repository geolysis ./dist/*

RESOURCE_PATH := ./geolysis/ui/assets

rc:
	pyside6-rcc $(RESOURCE_PATH)/resources.qrc -o $(RESOURCE_PATH)/resources_rc.py

run:
	py ./geolysis/ui/main.py
