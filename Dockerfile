FROM python:3.10.9-slim-buster
LABEL maintainer="spacix@gmail.com"

RUN mkdir /app
WORKDIR app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

