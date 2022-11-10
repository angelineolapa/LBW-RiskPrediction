FROM python:3.9-slim

RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", ".", "./"]

RUN pipenv install --system --deploy

EXPOSE 9696

CMD gunicorn app:server
