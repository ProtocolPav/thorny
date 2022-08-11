import asyncpg
from sanic import Sanic, Request
from sanic.response import json as sanicjson
from datetime import datetime
from connection_pool import create_pool
from dbutils import WebserverUpdates

app = Sanic("thorny_server_app")
pool: asyncpg.Pool


@app.listener('after_server_start')
async def create_database_pool(sanic, loop):
    global pool
    pool = await create_pool(loop)


@app.route('/')
async def test(request: Request):
    return sanicjson({'hello': 'world'})


@app.post('/<gamertag:str>/connect')
async def connect(request: Request, gamertag: str):
    gamertag = gamertag[12:-3].replace("%20", " ")
    datetime_object = datetime.strptime(request.body.decode('ascii'), "%Y-%m-%d %H:%M:%S")
    async with pool.acquire() as conn:
        await WebserverUpdates.connect(gamertag, datetime_object, conn)
    return sanicjson({"Accept": True})


@app.post('/<gamertag:str>/disconnect')
async def disconnect(request: Request, gamertag: str):
    gamertag = gamertag[12:-3].replace("%20", " ")
    datetime_object = datetime.strptime(request.body.decode('ascii'), "%Y-%m-%d %H:%M:%S")
    async with pool.acquire() as conn:
        await WebserverUpdates.disconnect(gamertag, datetime_object, conn)
    return sanicjson({"Accept": True})
