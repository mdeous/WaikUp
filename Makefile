WAIKUP_VERSION := $(shell git rev-parse --abbrev-ref HEAD | cut -d'/' -f2)

all: latest

latest:
	docker build -t mdeous/waikup:latest .

release:
	docker build -t mdeous/waikup:${WAIKUP_VERSION} .

dev:
	docker build -f Dockerfile-devel -t mdeous/waikup:dev .

run:
	WAIKUP_VERSION=${WAIKUP_VERSION} docker-compose up

run-dev:
	docker-compose -f docker-compose-dev.yml up
