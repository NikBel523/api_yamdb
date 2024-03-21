## Бэкенд YamDb

Представляет REST-сервис бэкенда для работы с отзывами на произведения и подсчёту рейтинга. Включает регистрацию пользователей, простой профайл и безопасность доступа на основе JWT-токена, получаемого по коду подтверждения на почту. Позволяет идентифицированным пользователем:

- создавать и редактировать произведения, привязанные к категориям и жанрам;
- добавлять и редактировать отзывы ко всем произведениям;
- ставить произведениям оценки и добавлять ревью;
- комментировать ревью.

### Билд проекта

1. Взятие исходников из репозитория:

    `git clone git@github.com:alexf2/api_yamdb.git` или

    `git clone https://github.com/alexf2/api_yamdb.git`.

2. Перехдим в корень проекта:

    `cd api_yamdb`.

3. Создаём виртуальное окружение:

      **Важно!** Должен быть установлен Python 3.9.
      `python3 -m venv venv`

4. Активируем созданное виртуальное окружение:

    Windows: `venv/Scripts/activate`;

    Linux: `source env/bin/activate`.

5. Опциально обновляем pip:

    `python3 -m pip install --upgrade pip`.

6. Ставим зависимости:

    `cd ./yatube_api`;

    `pip install -r requirements.txt`.

7. Добавляем супер-пользователя.

    `python manage.py createsuperuser`.

8. Накатываем миграции:

    `python manage.py migrate`.

9. Заливаем тестовые данные:

    `cd api_yamdb`

    `python import_csv.py`

10. Стартуем сервис:

    `python3 manage.py runserver`.

### Swagger для Api

После запуска сервиса доступен на: [Swagger](http://127.0.0.1:8000/redoc/).

### Регистрация пользователя

    `POST /api/v1/auth/signup/`
в теле:

```json
{
    "email": "user@example.com",
    "username": "string"
}
```

В результате на почту приходит код. Далее, по коду нужно получить JWT-токен.
    `POST /api/v1/auth/tiken/`
в теле:

```json
{
  
    "username": "string",
    "confirmation_code": "string"
}
```

С токеном можно получить свой профайл:
    `GET /api/v1/users/me`
В http-header передать токен:

```
  Authorization = Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA5ODQ5MzE2LCJqdGkiOiIwYjFlNTJiYmMyN2Q0YzA4YTk2NTRmNGEzYmQ2ZGE2NyIsInVzZXJfaWQiOjJ9.EfF6Aso6VBGaWn5KO5FO4jt3NmuV41BaCtqktgxE1fE
```

Респонс:

```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

[© Team Three](https://github.com/alexf2/api_yamdb)
