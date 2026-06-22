FROM python:3.13-alpine

COPY . /thorny/

COPY ./nexuscore-client ./nexuscore-client

RUN pip install -r /thorny/requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/thorny/"

WORKDIR /thorny/src

CMD ["python", "-u", "thorny.py"]
