FROM python:latest

COPY requirements.txt /thorny/thorny_core/requirements.txt

RUN pip install -r /thorny/thorny_core/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/thorny/"

WORKDIR /thorny/thorny_core