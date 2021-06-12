![pep8 codestyle](https://github.com/ivartm/bbbs/actions/workflows/codestyle.yml/badge.svg)

[![afisha app tests](https://github.com/ivartm/bbbs/actions/workflows/tests.yml/badge.svg)](https://github.com/ivartm/bbbs/actions/workflows/tests.yml)

# bbbs
Бэкенд для проекта Старшие Братья Старшие Сестры https://www.nastavniki.org/


#### Технологии и требования
Django
Django REST Framework
Poetry
*дополнить*

### Установка локально
Установите [poetry](https://python-poetry.org/docs/)
Установкой локального окружения и зависимости занимается poetry

```shell
git clone git@github.com:ivartm/bbbs.git
cd bbbs
poetry shell
poetry install --no-root
```

### Добавление пакета и зависимостей
Детальное описание в [документации poetry](https://python-poetry.org/docs/cli/)

Если кратко, то добавить пакет в список зависимостей для Production
```shell
poetry add {название пакета}
```

Установка пакета в окружение разработки:
```shell
poetry add --dev {название пакета}
```

### Настройки проекта
Разделены на 3 ветки **prod, dev, local**, находят в config/settings
Корневые настройки в base.txt, добавляйте пакеты и настройки с разумно.

Хорошая практика при разработке своей ветки использовать local.txt
После окончания тестирования переносить в dev, prod, base в зависимости от значимости.

### Запуск проекта
По умолчанию проект запускается с локальными настройками в confg.settings.local

Запуск с определенной конфигурацией:
./manage.py runserver --settings=config.settings.dev

### Создание фикстур

Всё что ниже ждёт обновления
>
Создает предустановленные города
Создает 200 записей участников на мероприятия (в процессе создания создает события и пользователей)


```shell
make shell
```

```python
from common.fixtures import make_fixtures
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