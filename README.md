# Проект Api YamDB

Проект выполнен командой из трёх человек:

## [Максим](https://github.com/khekhnev)

## [Ирина](https://github.com/alicezweig)

[Федор](https://github.com/thedross)


## Проект **YaMDb** собирает отзывы пользователей на различные произведения.

Взаимодействие с проектом реализовано через API.

Полная документация по API доступна в файле [redoc.yaml](api_yamdb/static/redoc.yaml)

### Список использованных технологий при разработке: 


`Python` 

`Django`

`djangorestframework`

`djangorestframework-simplejwt` 

`requests`


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/thedross/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
