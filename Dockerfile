FROM python:3.10.7-alpine

COPY requirements.txt /temp/requirements.txt
COPY gym_tracker /gym_tracker
WORKDIR /gym_tracker
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-user

USER service-user