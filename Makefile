run:
	mkdir -p tmp
	docker-compose up -d

build:
	docker-compose build

stop:
	docker-compose stop

reset:
	docker-compose stop
	rm -rf tmp

br: build run
