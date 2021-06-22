runserver:
	python manage.py runserver

build-static:
	python manage.py collectstatic --noinput

migrate:
	python manage.py makemigrations
	python manage.py migrate

filldb:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py filldb
	python manage.py migrate

filldb-with-superuser:

	python manage.py makemigrations
	python manage.py migrate
	python manage.py filldb
	python manage.py migrate
	python manage.py createsuperuser

createsuperuser:
	python manage.py createsuperuser

shell:
	python manage.py shell_plus

configurelocaly:
	poetry shell
	poetry install --no-root
	pre-commit install

gen-secretkey:
	python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
