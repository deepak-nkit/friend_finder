FROM python:3.12

RUN mkdir app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

WORKDIR /app
COPY ./app /app/app


