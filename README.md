# bbbs
Бэкенд для проекта Старшие Братья Старшие Сестры https://www.nastavniki.org/

Запуск с определенной конфигурацией:
./manage.py runserver --settings=config.settings.dev
./manage.py <любая команда> --settings=config.settings.dev

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

Запуск django сервера в dev 

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

Запуск shell plus (должен быть установлен)

```shell
make shell
```
