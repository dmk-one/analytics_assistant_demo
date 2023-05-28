FROM python:3.8-buster

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TZ=Asia/Almaty
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


WORKDIR /app
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install nano
RUN pip install --upgrade pip
COPY ./dockers/django/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
