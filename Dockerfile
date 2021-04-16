FROM python:3.9

RUN pip install gunicorn webob parse
WORKDIR /app
COPY . .
