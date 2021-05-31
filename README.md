![pep8 codestyle](https://github.com/ivartm/bbbs/actions/workflows/codestyle.yml/badge.svg)

[![afisha app tests](https://github.com/ivartm/bbbs/actions/workflows/tests.yml/badge.svg)](https://github.com/ivartm/bbbs/actions/workflows/tests.yml)

# bbbs
Бэкенд для проекта Старшие Братья Старшие Сестры https://www.nastavniki.org/

По умолчанию проект запускается с локальными настройками в confg.settings.local

Установки для запуска в локальном окружении:
```shell
python -m pip install --upgrade pip
pip install -r requirements/local.txt
```

Запуск с определенной конфигурацией:
./manage.py runserver --settings=config.settings.dev

### Создание фикстур

Создает предустановленные города
Создает 200 записей участников на мероприятия (в процессе создания создает события и пользователей)

```shell
make shell
```

```python
from afisha.fixtures import make_fixtures
make_fixtures()
````

### В проект добавлен Makefile для облегчения запуска management команд в DEV окружении

Подготовка локального окружения
```shell
configurelocaly
```

Запуск django сервера c локальными настройками

```shell
make runserver
```

Собрать статику

```shell
make build-static
```

Заполнить базу тестовыми данными (из фикстур в файле, скоро дополним)
```shell
make fill-db
```

Создать и применить миграции, без заполнения данными
```shell
make migrate
```

Создать суперпользователя:
```shell
make createsuperuser
```

Запуск shell plus (должен быть установлен)

```shell
make shell
```

# Запуск тестов

```shell
pytest
```
# Просмотр автодокументации по API 

```shell
.../api/schema/
.../api/schema/swagger-ui/,
.../api/schema/redoc/,
```