FROM python:3.9.5
WORKDIR /code
COPY requirements/ requirements/
RUN pip3 install -r requirements/dev.txt
COPY . .
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
