FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

COPY . .

RUN pip install -r requirements.txt
