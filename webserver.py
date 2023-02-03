from sanic import Sanic, Request
from sanic.response import json as sanicjson
from datetime import datetime
import asyncio

from thorny import thorny as client, TOKEN, birthday_checker, interruption_check, day_counter
from thorny_core.db.poolwrapper import pool_wrapper
from thorny_core.db import event, UserFactory, GuildFactory


app = Sanic("thorny_bot_app")


@app.route('/')
async def test(request: Request):
    return sanicjson({'hello': 'world'})


@app.post('/<guild_id:str>/<gamertag:str>/connect')
async def connect(request: Request, gamertag: str, guild_id: str):
    gamertag = gamertag[12:-3].replace("%20", " ")
    guild_id = int(guild_id[12:-3])

    thorny_guild = await GuildFactory.build(client.get_guild(guild_id))
    thorny_user = await UserFactory.build(thorny_guild.discord_guild.get_member(await UserFactory.get_user_by_gamertag(gamertag,
                                                                                                                       guild_id)))
    connection = event.Connect(client, datetime.now(), thorny_user, thorny_guild)
    await connection.log()
    return sanicjson({"Accept": True})


@app.post('/<guild_id:str>/<gamertag:str>/disconnect')
async def disconnect(request: Request, gamertag: str, guild_id: str):
    gamertag = gamertag[12:-3].replace("%20", " ")
    guild_id = int(guild_id[12:-3])

    thorny_guild = await GuildFactory.build(client.get_guild(guild_id))
    thorny_user = await UserFactory.build(thorny_guild.discord_guild.get_member(await UserFactory.get_user_by_gamertag(gamertag,
                                                                                                                       guild_id)))
    disconnection = event.Disconnect(client, datetime.now(), thorny_user, thorny_guild)
    await disconnection.log()
    return sanicjson({"Accept": True})


@app.post('/<guild_id:str>/disconnect/all')
async def disconnect_all(request: Request, guild_id: str):
    guild_id = int(guild_id[12:-3])
    thorny_guild = await GuildFactory.build(client.get_guild(guild_id))
    for connected_user in await thorny_guild.get_online_players():
        thorny_user = await UserFactory.build(thorny_guild.discord_guild.get_member(connected_user['user_id']))
        disconnection = event.Disconnect(client, datetime.now(), thorny_user, thorny_guild)
        await disconnection.log()

    return sanicjson({"Accept": True})


@app.listener('after_server_start')
async def start_bot(application: Sanic):
    asyncio.get_event_loop().create_task(coro=client.start(token=TOKEN, reconnect=True),
                                         name="Thorny Discord Client")

    birthday_checker.start()
    day_counter.start()
    # interruption_check.start()

    await pool_wrapper.init_pool()

app.run(host="0.0.0.0")
