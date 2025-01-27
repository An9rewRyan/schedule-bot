# pull official base image
FROM python:3.11.3
# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY . /usr/src/app/Ï
COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN pip install -r requirements.txt
RUN alembic revision --autogenerate
RUN alembic upgrade head
