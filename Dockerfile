FROM python:3.12.7-bookworm

COPY requirements.txt /thorny/thorny_core/requirements.txt

RUN pip install -r /thorny/thorny_core/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/thorny/"

WORKDIR /thorny/thorny_core