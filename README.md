# Документация к API проекту YAMDB (v1.01)
Проект YaMDb собирает отзывы пользователей на различные произведения.

![yamdb_final workflow](https://github.com/atl40Nikolay/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Оглавление
0. [Описание](#описание)
1. [Стек технологий](#стек-технологий)
2. [Как запустить проект](#как-запустить-проект)
3. [Примеры запросов к api](#примеры-запросов-к-api)
4. [Авторы проекта](#авторы-проекта)


## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Произведению может быть присвоен жанр. Новые жанры и категории может создавать только администратор. Читатели оставляют к произведениям текстовые отзывы и выставляют произведению оценку в диапазоне от одного до десяти. Nз множества оценок автоматически высчитывается рейтинг - средняя оценка произведения.


## Стек технологий
- проект написан на Python с использованием Django REST Framework
- библиотека Simple JWT - работа с JWT-токеном
- библиотека django-filter - фильтрация запросов
- базы данныx - PostgreSQL
- система управления версиями - git
- gunicorn HTTP сервер для UNIX
- nginx HTTP-сервер и обратный прокси-сервер
- Docker инструмент для создания контейнеров, в которых работают ваши приложения.


## Как запустить проект:

- Клонировать репозиторий и перейти в директорию с docker-compose.yaml в командной строке:
```
git clone https://github.com/atl40Nikolay/infra_sp2.git
cd infra_sp2/infra
``` 
- Развернуть докер-контейнеры:
```
docker-compose up -d --build
```
- Выполнить миграции в контейнере web
```
docker-compose exec web python manage.py migrate
```
- Создать суперюзера в контейнере (ввести username, email, password)
```
docker-compose exec web python manage.py createsuperuser
```
- Собрать статику в контейнере web
```
docker-compose exec web python manage.py collectstatic --no-input
```
- Ознакомиться с документацией по адресу.
[http://127.0.0.1/redoc/](http://127.0.0.1/redoc/)
- При необходимости сохранить дамп БД из контейнера
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```
- Шаблон для заполнения env-файла
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```

## Примеры запросов к api

### Некоторые примеры запросов к API.
Доступные энд-поинты:
GET-запросы

```
/api/v1/titles/
```
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
```
/api/v1/categories/
```
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
```
/api/v1/genres/
```
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
```
/api/v1/titles/{title_id}/reviews/
```
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
POST-запрос
Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.
```
/api/v1/titles/{title_id}/reviews/
```
```
{
  "text": "string",
  "score": 10
}
```

## Авторы проекта

Николай Журавлёв
atl40@yandex.ru
