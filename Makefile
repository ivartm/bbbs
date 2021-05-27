runserver:
	python manage.py runserver --settings=config.settings.dev

build-static:
	python manage.py collectstatic --noinput

fill-db:
	python manage.py makemigrations --settings=config.settings.dev
	python manage.py migrate --settings=config.settings.dev
	python manage.py createsuperuser --settings=config.settings.dev
	python manage.py loaddata --settings=config.settings.dev fixtures.json

shell:
	python manage.py shell_plus --settings=config.settings.dev

runtest:
	python manage.py test --settings=config.settings.dev
