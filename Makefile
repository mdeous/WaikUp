all: build

build:
	docker build -t mdeous/waikup:latest .

run:
	WAIKUP_VERSION=${WAIKUP_VERSION} docker-compose up
