WAIKUP_VERSION := $(shell git rev-parse --abbrev-ref HEAD | cut -d'/' -f2)

all: latest

latest:
	docker build -t mdeous/waikup:latest .

release:
	docker build -t mdeous/waikup:${WAIKUP_VERSION} .

devel:
	docker build -f Dockerfile-devel -t mdeous/waikup:devel .

run:
	WAIKUP_VERSION=${WAIKUP_VERSION} docker-compose up

run-devel:
	docker-compose -f docker-compose-devel.yml up
