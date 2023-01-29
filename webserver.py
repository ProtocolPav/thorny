import asyncpg as pg
from sanic import Sanic, Request
from sanic.response import json as sanicjson
from datetime import datetime
# from dbutils import WebserverUpdates, Base
import asyncio
import json


app = Sanic("thorny_server_app")
pool: pg.Pool


async def create_pool(loop=None):
    config = json.load(open('../thorny_data/config.json', 'r+'))
    pool_object = await pg.create_pool(database=config['database']['name'],
                                       user=config['database']['user'],
                                       password=config['database']['password'],
                                       host=config['database']['host'],
                                       port=5432,
                                       max_inactive_connection_lifetime=10.0,
                                       max_size=300,
                                       loop=loop)
    return pool_object


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
    asyncio.get_event_loop().create_task(coro=thorny.start(TOKEN),
                                         name="Thorny Discord Client")

    global pool
    pool = await create_pool()

    while True:
        print("TASKS LIST", asyncio.all_tasks(asyncio.get_running_loop()))
        await asyncio.sleep(10)

app.run(host="0.0.0.0")
