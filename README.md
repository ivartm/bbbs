[![CI/CD](https://github.com/ivartm/bbbs/actions/workflows/build_and_deploy.yaml/badge.svg)](https://github.com/ivartm/bbbs/actions/workflows/build_and_deploy.yaml)
[![codecov](https://codecov.io/gh/ivartm/bbbs/branch/main/graph/badge.svg?token=30U7Y04CUE)](https://codecov.io/gh/ivartm/bbbs)
![pep8 codestyle](https://github.com/ivartm/bbbs/actions/workflows/codestyle.yaml/badge.svg)

## https://bbbs.fun/
# bbbs
Бэкенд для проекта Старшие Братья Старшие Сестры https://www.nastavniki.org/


## Технологии и требования
```
Python 3.9+
Django
Django REST Framework
Poetry
Docker
Factory-Boy
```

**Проект предполагает 2 типа запуска: локально и в полноценном режиме. В обоих случаях используется docker. В обоих случаях нужно задать переменные окружения.**

1. Запуск локально — в docker используется только база данных (PostgreSQL). Пример использования — local.yaml
2. Запуск в полноценном режиме — в docker будут помещены БД, код проекта, статика и медиа раздается nginx. Пример использования — production.yam

#### Переменные окружения
Контейнерам нужны переменные окружения для хранения секретов.
Структура переменных окружения (разделение для локального запуска и в продакшн):
```
.envs/
├── .local
│   ├── .env
└── .prod
    ├── .django
    └── .postgres
```

## Установка локально с БД в Docker
1. Сколонируйте репозиторий проекта и перейдите в папку проекта:
    ```shell
    git clone git@github.com:ivartm/bbbs.git
    cd bbbs
    ```
2. Установите рабочее окружение и зависимости (управляются через [poetry](https://python-poetry.org/docs/)). Файлы **requirements** вручную редактировать не нужно
    ```shell
    poetry shell
    poetry install --no-root
    pre-commit install
    ```
3. Убедитесь что установлен и запущен **docker** и **docker-compose**
4. Запустите контейнер с БД:
    ```shell
    docker-compose -f local.yaml up --build -d
    ```

5. Локальный сервер не будет работать корректно без API ключей Mailjet и Youtube. Задайте их в переменных окружения:

  - создайте в корне проекта файл '.env', скопируйте в него содержимой файла '.envs example/.local/.env'
  - укажите значение ключей. Их можно узнать у вашей команды

6. Зпустите проект, он будет использовать БД в контейнере:
    ```python
    python manage.py runserver
    ```
7. Остановить контейнер с БД:
    ```shell
    docker-compose -f local.yaml down
    ```
8. Остановить контейнер с БД удалив данные:
    ```shell
    docker-compose -f local.yaml down --volumes
    ```

## CI/CD и продакшн
Используется github Actions, workflow **build_and_deploy.yaml**
Чтобы проект развернулся и работала автоматизация выполните шаги:

1. Склонируйте папку проекта на сервер
    ```shell
    git clone git@github.com:ivartm/bbbs.git
    cd bbbs
    ```

2. Задайте переменные окружения. Какие именно переменные нужны и как их задавать в папке '.envs example'
    ```
    .envs/
    └── .prod
        ├── .django
        └── .postgres
    ```

3. В github создайте **environment** назвав его "production_environment" и задайте ключи доступа к github и серверу
    - COMPOSE_FILE
    - DOCKER_PASSWORD
    - DOCKER_USERNAME
    - HOST
    - SSH_KEY
    - USERNAME
4. При следующем пуше в ветку "main", если тесты пройдены успешно проект будет выгружен на сервер и перезапущен


## Примеры работы с docker:

1. Чтоб не указывать файл yaml каждый раз его можно сохранить в env:
    ```bash
    export COMPOSE_FILE=local.yaml # тут экспортировали файл для локальной разработки
    docker-compose up --build -d
    ```
2. Выполнить команду внутри контейнера:
    ```bash
    docker-compose exec {контейнер в котором выполнить} {команда}
    ```
3. Например заполнить базу тестовыми данными:
    ```bash
    docker-compose exec django python manage.py filldb
    ```
4. Или создать только 200 мероприятий базу тестовыми данными:
    ```bash
    docker-compose exec django python manage.py filldb --event 200
    ```
5. Создать суперпользователя:
    ```bash
    docker-compose exec django python manage.py createsuperuser
    ```
6. Как смотреть что происходит в контейнерах:
    1. Запустить контейнеры интерактивно (**не использовать** флаг -d (--detach , -d)):
        ```bash
        docker-compose up
        ```
    2. Если контейнеры уже запущены в фоновом режим, то можно выводить журнал. Например контейнера django:
        ```bash
        docker-compose logs --follow django
        ```

## Работа с зависимостями и пакетами
Управляется **poetry**. Детальное описание в [документации poetry](https://python-poetry.org/docs/cli/)

Если кратко, то:
- добавить пакет в список зависимостей для **Production**
```shell
poetry add {название пакета}
```

- установить пакет в **окружение разработки** (dev):
```shell
poetry add --dev {название пакета}
```

- обновить список зависимостей:
```shell
poetry update
```

- узнать путь до интепретатора:
```shell
poetry env info --path
```

## Pre-commit хуки
Настроена интеграций с pre-commit для проверки кода и более простой интеграции с CI/CD.

Выполняются:

- стандартные хуки для общего качества кода
    - id: trailing-whitespace
    - id: end-of-file-fixer
    - id: check-yaml
    - id: check-added-large-files
    - id: check-merge-conflict
- проверка PEP8 flake8
- сортировка импортов isort (поддержка формата black)
- проверка PEP8 black
- если есть изменения в **poetry.lock** или **pyproject.toml**, то обновляются файлы с зависимостями в **requirements/**. Добавляйте изменения в коммит.

Выполнить pre-commit хуки локально:
```shell
pre-commit run ----all-files
```

Обновить версии репозиториев с pre-commit хуками:
```shell
pre-commit autoupdate
```


## Настройки проекта settings
Разделены на 3 ветки **prod.py, dev.py, local.py**, находятся в **config/settings** Корневые настройки в **base.py**

Хорошая практика при разработке использовать local.py.
После окончания тестирования переносить в dev, prod, base в зависимости от значимости.

## Запуск проекта
По умолчанию проект запускается с локальными настройками в confg.settings.local

Запуск с определенной конфигурацией:
```python
python manage.py runserver --settings=config.settings.dev
```

## Заполнение базы данных тестовыми данными

Запуск с предустановленными параметрами:

- все города из предустановленного списка + 10 случайных
- 200 случайных событий
- 15 случайных кураторов
- 10 случайных тегов для Права ребенка
- 70 случайных Прав ребенка с 1 до 5 тегов (случайным образом)
- 70 случайных пользователей, который зарегистрированы на 0-5 мероприятий
- 15 тегов для Вопросы
- 70 случайных Вопросов с 1 до 15 тегов (случайным образом)
- 5 Вопросов без тегов
- 5 Вопросов без ответов
- 15 тегов "Куда пойти"
- 70 случайных "Куда пойти" с 1 до 5 тегов (случайным образом)
- 70 статей в Справочнике
- 10 случайных тегов для Фильмов
- Фильмы с 1 до 5 тегами из сохраненного списка links (случайные данные не подходят: ссылки не будут работать)
- 50 записей в дневнике для случайных пользователей
- 70 случайных статей в "Статьи"
- 2 тега для книг: Художественные и Научные
- 50 случайных книг
- 15 случайных тегов для "Видео"
- Видео с 1 до 5 тегами из сохраненного списка links (случайные данные не подходят: ссылки не будут работать)
- 30 случайных "История дружбы"
- 100 случайных картинок для "История дружбы"
- главную страницу


```python
./manage.py filldb
```
так же есть возможность опционально добавлять тестовые данные, подробности в help:
```python
./manage.py filldb --help
```
для очистки таблиц БД (но не удаление!) можете воспользоваться стандартной командой Django:
```python
./manage.py flush
```

## В проект добавлен Makefile для облегчения запуска management команд в DEV окружении

Запуск django сервера c локальными настройками
```shell
make runserver
```

Собрать статику
```shell
make build-static
```

Заполнить базу тестовыми данными:
```shell
make filldb
```

БД + создать суперпользователя (запросит реквизиты):
```shell
make filldb-with-superuser:
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

Сгенерирвоать новый SECRET_KEY и показать его на экране:
```shell
make gen-secretkey
```

## Запуск тестов

```shell
pytest
```
## Просмотр автодокументации по API

```shell
.../swagger/
.../redoc/,
```
