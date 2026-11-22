# District Clone

A web app for booking events, based on District by Zomato. Customers can book event slots using a wallet. Organizers can create events and manage tickets.

Live: http://54.206.167.18/

## Features

Customers:
- Sign up and log in
- Add money to wallet and view transactions
- Browse events and book slots
- View their tickets

Organizers:
- Create events and slots
- View tickets and mark them as consumed
- See tickets sold and revenue for each event

## Tech stack

Django, PostgreSQL, uv, Gunicorn, Nginx, Docker Compose, AWS EC2

## Run locally

```
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

Needs PostgreSQL and the environment variables `SECRET_KEY`, `DEBUG` and `DB_PASSWORD`.

## Run with Docker

```
docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Open http://localhost/
