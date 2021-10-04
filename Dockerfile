FROM python:3.8

ARG APP_DIR=app


ADD . /$APP_DIR
WORKDIR /$APP_DIR

RUN pip install -r requirements.txt



