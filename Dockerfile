FROM python:3.12.7-bookworm

COPY requirements.txt /thorny_core/requirements.txt

RUN pip install -r /thorny_core/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/thorny_core/"

WORKDIR /thorny_core