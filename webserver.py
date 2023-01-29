from sanic import Sanic, Request
from sanic.response import json as sanicjson
from datetime import datetime
# from dbutils import WebserverUpdates, Base
import asyncio

from thorny import thorny as client, TOKEN

from thorny_core.db.poolwrapper import pool_wrapper


app = Sanic("thorny_server_app")


@app.route('/')
async def test(request: Request):
    return sanicjson({'hello': 'world'})


@app.post('/<gamertag:str>/connect')
async def connect(request: Request, gamertag: str):
    gamertag = gamertag[12:-3].replace("%20", " ")
    datetime_object = datetime.strptime(request.body.decode('ascii'), "%Y-%m-%d %H:%M:%S")
    # thorny_user = await UserFactory.build(client.get_user(await UserFactory.get_user_by_gamertag(gamertag)))
    # print(thorny_user)
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


@app.listener('after_server_start')
async def start_bot(application):
    print("starting bot...")
    asyncio.get_event_loop().create_task(coro=client.start(TOKEN),
                                         name="Thorny Discord Client")

    await pool_wrapper.init_pool()

app.run(host="0.0.0.0")
