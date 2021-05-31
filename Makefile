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
	python manage.py loaddata fixtures_by_factory_boy.json
	python manage.py createcustomsuperuser

createsuperuser:
	python manage.py createsuperuser

shell:
	python manage.py shell_plus

configurelocaly:
	python -m pip install --upgrade pip
	pip install -r requirements/local.txt
