# Django — full-stack web framework

> Django provides URL routing, models, migrations, forms, authentication, templates, and an administrative interface.

## Install and start

```bash
python -m pip install django
python -m django startproject config .
python manage.py runserver
```

The development server is not a production server. Keep `SECRET_KEY` out of source control, set `DEBUG=False` in production, configure `ALLOWED_HOSTS`, and use a real deployment server and database.

## A view

```python
# app/views.py
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})
```

Wire views through `urls.py`, use migrations for schema changes, and protect state-changing requests with Django's CSRF mechanisms. Prefer the ORM's parameterization over manually assembled SQL.

Next door: [SQLAlchemy](092-sqlalchemy.md) when you need a framework-independent ORM.
