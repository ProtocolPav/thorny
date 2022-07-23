FROM python:latest

RUN pip install asyncpg
RUN pip install sanic

EXPOSE 8000

