FROM python:3.9.9-slim

WORKDIR /usr/src/app/

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .