from sanic import Sanic, Request
from sanic.response import json as sanicjson
from datetime import datetime
import asyncio
import asyncpg as pg
import json
import httpx

app = Sanic("thorny-bot-app")

class PoolWrapper:
    __pool: pg.Pool

    async def init_pool(self):
        config = json.load(open('../thorny_data/config.json', 'r+'))
        self.__pool = await pg.create_pool(database=config['database']['name'],
                                         user=config['database']['user'],
                                         password=config['database']['password'],
                                         host=config['database']['host'],
                                         port=5432,
                                         max_inactive_connection_lifetime=10.0,
                                         max_size=300,
                                         loop=None)

    def connection(self):
        return self.__pool.acquire()

webserver_pool = PoolWrapper()


@app.route('/')
async def test(request: Request):
    return sanicjson({'hello': 'world'})


@app.route('/preemption/warning')
async def preempt(request: Request):
    async with httpx.AsyncClient() as client:
        r = await client.get(f"http://thorny-bds:8000/server/preempt", timeout=None)

    return sanicjson({'server': 'preempted'})


@app.post('/<guild_id:str>/<gamertag:str>/connect')
async def connect(request: Request, gamertag: str, guild_id: str):
    async with webserver_pool.connection() as conn:
        gamertag = gamertag[12:-3].replace("%20", " ")
        guild_id = int(guild_id[12:-3])

        await conn.execute("""
                           INSERT INTO webserver.webevent(event_time, event, description)
                           VALUES($1, $2, $3)
                           """,
                           datetime.now(), 'connect', f'{guild_id},{gamertag}')

        print(f'[WEBSERVER] Sent Connect Event for processing...')
    return sanicjson({"Accept": True})


@app.post('/<guild_id:str>/<gamertag:str>/disconnect')
async def disconnect(request: Request, gamertag: str, guild_id: str):
    async with webserver_pool.connection() as conn:
        gamertag = gamertag[12:-3].replace("%20", " ")
        guild_id = int(guild_id[12:-3])

        await conn.execute("""
                           INSERT INTO webserver.webevent(event_time, event, description)
                           VALUES($1, $2, $3)
                           """,
                           datetime.now(), 'disconnect', f'{guild_id},{gamertag}')

        print(f'[WEBSERVER] Sent Disconnect Event for processing...')

    return sanicjson({"Accept": True})


@app.post('/<guild_id:str>/disconnect/all')
async def disconnect_all(request: Request, guild_id: str):
    async with webserver_pool.connection() as conn:
        guild_id = int(guild_id[12:-3])

        await conn.execute("""
                           INSERT INTO webserver.webevent(event_time, event, description)
                           VALUES($1, $2, $3)
                           """,
                           datetime.now(), 'disconnect all', f'{guild_id}')

        print(f'[WEBSERVER] Sent Disconnect All Event for processing...')

    return sanicjson({"Accept": True})


@app.get('/<guild_id:str>/commands/server')
async def server_commands(request: Request, guild_id: str):
    async with webserver_pool.connection() as conn:
        guild_id = int(guild_id[12:-3])

        command_list = await conn.fetch("""
                                        SELECT * FROM webserver.commands
                                        WHERE type = 'server'
                                        AND executed = false
                                        AND failed = false
                                        AND guild_id = $1
                                        ORDER BY schedule ASC
                                        """, guild_id)

    return sanicjson({"commands": command_list})


@app.listener('after_server_start')
async def start_bot(application: Sanic, loop: asyncio.AbstractEventLoop):
    # await client.login(TOKEN)
    # await application.add_task(client.connect(reconnect=True), name="Thorny Discord Client")
    # asyncio.get_event_loop().create_task(coro=client.connect(reconnect=True),
    #                                      name="Thorny Discord Client")
    #
    # birthday_checker.start()
    # day_counter.start()
    # interruption_check.start()

    await webserver_pool.init_pool()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, single_process=True)
