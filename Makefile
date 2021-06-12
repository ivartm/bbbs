runserver:
	python manage.py runserver

build-static:
	python manage.py collectstatic --noinput

migrate:
	python manage.py makemigrations
	python manage.py migrate

fill-db:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py loaddata fixtures.json
	python manage.py createsuperuser

createsuperuser:
	python manage.py createsuperuser

shell:
	python manage.py shell_plus

configurelocaly:
	poetry shell
	poetry install --no-root
