build:
	sudo docker-compose -f local.yml up --build -d --remove-orphans

b-build:
	sudo docker-compose -f local.yml up --build -d backend

up:
	sudo docker-compose -f local.yml up -d

down:
	sudo docker-compose -f local.yml down

show_logs:
	sudo docker-compose -f local.yml logs

migrate:
	sudo docker-compose -f local.yml run --rm backend python3 manage.py migrate

makemigrations:
	sudo docker-compose -f local.yml run --rm backend python3 manage.py makemigrations

collectstatic:
	sudo docker-compose -f local.yml run --rm backend python3 manage.py collectstatic --no-input --clear

run:
	sudo docker-compose -f local.yml run --rm backend python3 manage.py runserver

down-v:
	sudo docker-compose -f local.yml down -v


