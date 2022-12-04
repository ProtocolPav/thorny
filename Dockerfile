FROM python:3.10.8-buster

COPY requirements.txt /thorny/thorny_core/requirements.txt

RUN pip install -r /thorny/thorny_core/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/thorny/"

WORKDIR /thorny/thorny_core