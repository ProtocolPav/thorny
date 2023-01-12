import asyncpg as pg
from db.factory import create_pool
from sanic import Sanic, Request
from sanic.response import json as sanicjson
from datetime import datetime
from dbutils import WebserverUpdates, Base
from thorny_core.db.factory import UserFactory

app = Sanic("thorny_server_app")
pool: pg.Pool


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
    datetime_object = datetime.now().replace(microsecond=0)
    async with pool.acquire() as conn:
        await WebserverUpdates.disconnect(gamertag, datetime_object, conn)
    return sanicjson({"Accept": True})


@app.post('/<guild_id:str>/disconnect/all')
async def disconnect_all(request: Request, guild_id: str):
    print("Disconnecting all")
    guild_id = int(guild_id[12:-3])
    datetime_object = datetime.now().replace(microsecond=0)
    await WebserverUpdates.disconnect_all(guild_id, datetime_object)

    return sanicjson({"Accept": True})


# @app.listener('after_server_start')
# async def start_bot(application, loop: asyncio.AbstractEventLoop):
#     print("starting bot...")
#     loop.create_task(thorny.start(TOKEN))

app.run(host="0.0.0.0")
