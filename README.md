# yamdb_final_new
## Бэйдж

![workflow](https://github.com/gruand69/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Проект YaMDb

Проект YaMDb собирает отзывы пользователей на различные произведения такие как
фильмы, книги и музыка.

## Развёрнутый проект

http://gruand69.ddns.net/api/v1/, 
http://gruand69.ddns.net/admin/, 
http://gruand69.ddns.net/redoc/.

## Описание проекта:

API YaMDb позволяет работать со следующими сущностями:

* JWT-токен (Auth): отправить confirmation_code на переданный email, получить
  JWT-токен
  в обмен на email и confirmation_code;
* Пользователи (Users): получить список всех пользователей, создать
  пользователя,
  получить пользователя по username, изменить данные пользователя по username,
  удалить
  пользователя по username, получить данные своей учётной записи, изменить
  данные своей учётной записи;
* Произведения (Titles), к которым пишут отзывы: получить список всех объектов,
  создать
  произведение для отзывов, информация об объекте, обновить информацию об
  объекте, удалить произведение.
  пользователя по username, получить данные своей учётной записи, изменить
  данные своей учётной записи;
* Категории (Categories) произведений: получить список всех категорий, создать
  категорию, удалить категорию;
* Жанры (Genres): получить список всех жанров, создать жанр, удалить жанр;
* Отзывы (Review): получить список всех отзывов, создать новый отзыв, получить
  отзыв по id,
  частично обновить отзыв по id, удалить отзыв по id;
* Комментарии (Comments) к отзывам: получить список всех комментариев к отзыву
  по id, создать
  новый комментарий для отзыва, получить комментарий для отзыва по id, частично
  обновить комментарий к отзыву по id, удалить комментарий к отзыву по id.

## Стек технологий:

* [Python 3.7+](https://www.python.org/downloads/)
* [Django 2.2.16](https://www.djangoproject.com/download/)
* [Django Rest Framework 3.12.4](https://pypi.org/project/djangorestframework/#files)
* [Pytest 6.2.4](https://pypi.org/project/pytest/)
* [Simple-JWT 1.7.2](https://pypi.org/project/djangorestframework-simplejwt/)
* [pytest 6.2.4](https://pypi.org/project/pytest/)
* [pytest-pythonpath 0.7.3](https://pypi.org/project/pytest-pythonpath/)
* [pytest-django 4.4.0](https://pypi.org/project/pytest-django/)
* [djangorestframework-simplejwt 4.7.2](https://pypi.org/project/djangorestframework-simplejwt/)
* [Pillow 9.2.0](https://pypi.org/project/Pillow/)
* [PyJWT 2.1.0](https://pypi.org/project/PyJWT/)
* [requests 2.26.0](https://pypi.org/project/requests/)

## Как запустить проект:

Установка Docker 

Выполните установку docker для вашей операционной системы согласно инструкции на официальном сайте https://docs.docker.com/desktop/ 

### Шаблон env-файла

Secret - секрет Джанго

Данные БД Postgres: 

DB_ENGINE - движок postgres

DB_NAME - имя БД

POSTGRES_USER - пользователь БД

POSTGRES_PASSWORD - пароль БД

DB_HOST - название сервиса (контейнера)

DB_PORT - порт для подключения к БД 

### Запуск контейнеров:
Перед началом установки перейдите на компьютере в директорию с файлом docker-compose.yaml.

#### 1. Клонируйте проект:
```sh
git@github.com:gruand69/yamdb_final.git
```
#### 2. Разверните проект:
```sh
docker-compose up -d
```
#### 3. Создать суперпользователя:
```sh
docker-compose exec web python manage.py createsuperuser
```
#### 4. Импорт базы данных:
```sh
docker-compose exec web python manage.py dumpdata > дамп_бд.json
```

## Авторы:
[Антон Молчанов](https://github.com/antxrest)
[Андрей Грушевский](https://github.com/gruand69)
[Павел Туголуков](https://github.com/NakiriEri)
