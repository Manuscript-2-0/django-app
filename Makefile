env:
	pipenv shell

test:
	python manage.py test

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate