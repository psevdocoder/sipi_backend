#!/bin/bash
python manage.py migrate --noinput && \
python manage.py collectstatic --noinput && \
gunicorn -w 2 -b 0.0.0.0:8000 sipi_back.wsgi:application
