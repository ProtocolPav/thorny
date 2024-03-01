from sanic import Sanic, Request, text
from sanic.response import json as sanicjson
from datetime import datetime
import asyncio
import asyncpg as pg
import json
import httpx

app = Sanic("thorny-bot-app")

"""
GET retrieve all or just one resource.

POST is normally for create a new resource.

PUT used to update a resource

DELETE delete a resource
"""

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
    """
    Called by the GCP to warn the systems of preemption
    """
    async with httpx.AsyncClient() as client:
        r = await client.get(f"http://thorny-bds:8000/server/preempt", timeout=None)

    return sanicjson({'server': 'preempted'})


@app.post('/connect')
async def log_connect(request: Request):
    """
    Arguments: gamertag, guild_id
    :param request:
    :return:
    """
    async with webserver_pool.connection() as conn:
        if request.args.get('gamertag', None) and request.args.get('guild_id', None):
            gamertag = request.args['gamertag'][0]
            try:
                guild_id = int(request.args['guild_id'][0])

                await conn.execute("""
                                   INSERT INTO webserver.webevent(event_time, event, description)
                                   VALUES($1, $2, $3)
                                   """,
                                   datetime.now(), 'connect', f'{guild_id},{gamertag}')

                print(f'[WEBSERVER] Sent Connect Event for processing...')

            except TypeError:
                return text('Make sure guild_id is an integer')
        else:
            return text('Include args gamertag and guild_id. Example: thorny-wbs:8000/connect?gamertag=ABC&guild_id=123')
    return sanicjson({"Accept": True})


@app.post('/disconnect')
async def log_disconnect(request: Request):
    """
    Arguments: gamertag, guild_id
    :param request:
    :return:
    """
    async with webserver_pool.connection() as conn:
        if request.args.get('gamertag', None) and request.args.get('guild_id', None):
            gamertag = request.args['gamertag'][0]
            try:
                guild_id = int(request.args['guild_id'][0])

                await conn.execute("""
                                   INSERT INTO webserver.webevent(event_time, event, description)
                                   VALUES($1, $2, $3)
                                   """,
                                   datetime.now(), 'disconnect', f'{guild_id},{gamertag}')

                print(f'[WEBSERVER] Sent Connect Event for processing...')

            except TypeError:
                return text('Make sure guild_id is an integer')
        else:
            return text('Include args gamertag and guild_id. Example: thorny-wbs:8000/connect?gamertag=ABC&guild_id=123')
    return sanicjson({"Accept": True})


@app.post('/disconnect/all')
async def log_disconnect_all(request: Request):
    """
    Arguments: guild_id
    :param request:
    :return:
    """
    async with webserver_pool.connection() as conn:
        if request.args.get('guild_id', None):
            try:
                guild_id = int(request.args['guild_id'][0])

                await conn.execute("""
                                   INSERT INTO webserver.webevent(event_time, event, description)
                                   VALUES($1, $2, $3)
                                   """,
                                   datetime.now(), 'disconnect all', f'{guild_id}')

                print(f'[WEBSERVER] Sent Connect Event for processing...')

            except TypeError:
                return text('Make sure guild_id is an integer')
        else:
            return text('Include args guild_id. Example: thorny-wbs:8000/connect?gamertag=ABC&guild_id=123')
    return sanicjson({"Accept": True})


@app.get('/player/playtime')
async def get_playtime(request: Request):
    """
    Arguments: gamertag, guild_id
    :param request:
    :return:
    """
    ...


@app.get('/player/stats')
async def get_player_statistics(request: Request):
    """
    Arguments: gamertag, guild_id

    Returns the entirety of the player's statistics (blocks placed/broken, kills, deaths)
    :param request:
    :return:
    """
    ...


@app.post('/player/stats/block')
async def log_block_statistics(request: Request):
    """
    Arguments: gamertag, guild_id, operation(PLACE or BREAK), block_id, amount
    :param request:
    :return:
    """
    ...


@app.post('/player/stats/death')
async def log_death_statistics(request: Request):
    """
    Arguments: gamertag, guild_id, death_type
    :param request:
    :return:
    """
    ...


@app.post('/player/stats/kills')
async def log_kill_statistics(request: Request):
    """
    Arguments: gamertag, guild_id, entity_type (OPTIONAL), death_gamertag (OPTIONAL)
    :param request:
    :return:
    """
    ...


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
