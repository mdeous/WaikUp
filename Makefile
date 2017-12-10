all: build

build:
	docker build -t mdeous/waikup:${WAIKUP_VERSION:-develop} .

run:
	WAIKUP_VERSION=${WAIKUP_VERSION:-develop} docker-compose up
