FROM python:3.13-alpine

COPY . /thorny_core/

COPY ./nexuscore-client ./nexuscore-client

RUN pip install -r /thorny_core/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/thorny_core/"

WORKDIR /thorny_core

CMD ["python", "-u", "thorny.py"]
