all: latest

latest:
	docker build -t waikup:latest .

devel:
	docker build -f Dockerfile-devel -t waikup:devel .

run:
	docker-compose up

run-devel:
	docker-compose -f docker-compose-devel.yml up
