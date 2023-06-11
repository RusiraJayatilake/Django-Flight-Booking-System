FROM python:latest
WORKDIR /A2Core

RUN pip install django

CMD python manage.py runserver 0.0.0.0:8080