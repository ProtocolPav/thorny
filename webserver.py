import math

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


async def check_quest_progress(thorny_id: int, pos: tuple[int, int, int], event_type: str, ref: str, mainhand: str,
                               gamertag: str):
    async with webserver_pool.connection() as conn:
        current_quest = await conn.fetchrow("""
                                            SELECT * FROM thorny.userquests
                                            INNER JOIN thorny.quests ON thorny.quests.id = thorny.userquests.quest_id
                                            WHERE thorny.userquests.thorny_id = $1
                                            AND thorny.userquests.status is null
                                            """,
                                            thorny_id)

        if current_quest is not None and event_type == current_quest['objective_type']:
            # Checks if the objective is a part of the reference. Meaning, if the objective is copper_block
            # then weathered_copper_block would also be accepted
            ref_check = current_quest['objective'].split('minecraft:')[1] in ref

            # Check if a mainhand exists, the kill was done with that in hand
            if current_quest['required_mainhand'] is None:
                mainhand_check = True
            else:
                if current_quest['required_mainhand'] == mainhand:
                    mainhand_check = True
                else:
                    mainhand_check = False

            # Check if a location exists, the kill falls within the limits
            required_location = current_quest['required_location']
            if required_location is None:
                pos_check = True
            else:
                distance = math.sqrt((pos[0] - required_location[0])**2 + (pos[2] - required_location[1])**2)

                if distance <= current_quest['location_radius']:
                    pos_check = True
                else:
                    pos_check = False

            # Check that if a timer exists, the kill falls within the limits
            if current_quest['required_timer'] is None:
                timer_check = True
            elif current_quest['started_on'] is not None:
                if datetime.now() - current_quest['started_on'] < current_quest['required_timer']:
                    timer_check = True
                else:
                    timer_check = False
            else:
                timer_check = True

            # Check that if it is a mining quest, that the user didn't just place and mine the block
            if event_type == 'mine':
                block = await conn.fetchrow("""
                                            SELECT id FROM thorny.gamestats
                                            WHERE position_x = $1
                                            AND position_y = $2
                                            AND position_z = $3
                                            AND type = 'place'
                                            AND reference = $4
                                            """,
                                            pos[0], pos[1], pos[2], ref)

                if block:
                    block_check = False
                else:
                    block_check = True
            else:
                block_check = True

            if ref_check and mainhand_check and pos_check and timer_check and block_check:
                await conn.execute("""
                                   UPDATE thorny.userquests
                                   SET completion_count = completion_count + 1
                                   WHERE thorny_id = $1
                                   AND quest_id = $2
                                   """,
                                   thorny_id, current_quest['quest_id'])

                await conn.execute("""
                                   UPDATE thorny.userquests
                                   SET started_on = now()
                                   WHERE thorny_id = $1
                                   AND quest_id = $2
                                   AND started_on is null
                                   """,
                                   thorny_id, current_quest['quest_id'])

                async with httpx.AsyncClient() as client:
                    r = await client.get(f"http://thorny-bds:8000/commands/quest/progress?player={gamertag}&"
                                         f"progress=Quest%20Progress:%20"
                                         f"{current_quest['completion_count']+1}/{current_quest['objective_count']}",
                                         timeout=None)

                if current_quest['completion_count'] + 1 == current_quest['objective_count']:
                    async with httpx.AsyncClient() as client:
                        r = await client.get(f"http://thorny-bds:8000/commands/quest/complete?player={gamertag}&"
                                             f"reward={current_quest['item_reward']}&"
                                             f"reward_count={current_quest['item_reward_count']}",
                                             timeout=None)

                    await conn.execute("""
                                       UPDATE thorny.userquests
                                       SET status = True
                                       WHERE thorny_id = $1
                                       AND quest_id = $2
                                       """,
                                       thorny_id, current_quest['quest_id'])

                    if current_quest['balance_reward']:
                        await conn.execute("""
                                           UPDATE thorny.user
                                           SET balance = balance + $1
                                           WHERE thorny_user_id = $2
                                           """,
                                           current_quest['balance_reward'], thorny_id)


@app.post('/player/stats')
async def log_player_statistics(request: Request):
    """
    Arguments: gamertag, guild_id, posx, posy, posz, type, ref, mainhand

    type must be either one of: place, mine, kill, die
    ref will be either the block affected, entity affected or the cause of death if it is a fall for example

    Logs a player statistic. Based on world events.
    :param request:
    :return:
    """
    async with webserver_pool.connection() as conn:
        if request.args.get('gamertag', None) and request.args.get('guild_id', None):
            gamertag = request.args['gamertag'][0]
            try:
                guild_id = int(request.args['guild_id'][0])

                thorny_user = await conn.fetchrow("""
                                                  SELECT thorny.user.thorny_user_id FROM thorny.user
                                                  INNER JOIN thorny.profile
                                                  ON thorny.user.thorny_user_id = thorny.profile.thorny_user_id
                                                  WHERE whitelisted_gamertag = $1
                                                  AND thorny.user.guild_id = $2
                                                  """,
                                                  gamertag, guild_id)

                type = request.args.get('type', None)
                posx = int(request.args.get('posx', None))
                posy = int(request.args.get('posy', None))
                posz = int(request.args.get('posz', None))
                ref = request.args.get('ref', None)
                mainhand = request.args.get('mainhand', None)

                await conn.execute("""
                                   INSERT INTO thorny.gamestats(thorny_id, type, position_x, position_y, position_z, 
                                                                reference, mainhand, time)
                                   VALUES($1, $2, $3, $4, $5, $6, $7, $8)
                                   """,
                                   int(thorny_user['thorny_user_id']), type, posx, posy, posz, ref, mainhand, datetime.now()
                                   )


                print(f'[WEBSERVER] Log game stat {type}, {ref}')

                await check_quest_progress(thorny_user['thorny_user_id'], (posx, posy, posz), type, ref, mainhand,
                                           f'"{gamertag}"')
            except TypeError:
                return text('Make sure guild_id is an integer')
        else:
            return text('Include args gamertag and guild_id. Example: thorny-wbs:8000/connect?gamertag=ABC&guild_id=123')
    return sanicjson({"Accept": True})


@app.post('/chat/message')
async def relay_chat(request: Request):
    body = request.json
    config = json.load(open('../thorny_data/config.json', 'r+'))
    WEBHOOK_URL = config['webhook']

    async with httpx.AsyncClient() as client:
        r = await client.post(WEBHOOK_URL, timeout=None,
                              data={'content': f"{body['content']}",
                                    'username': f"[Server] {body['name']}"})

    return text('OK!')



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
