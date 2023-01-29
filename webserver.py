from sanic import Sanic, Request
from sanic.response import json as sanicjson
from datetime import datetime
import asyncio

from thorny import thorny as client, TOKEN
from thorny_core.db.poolwrapper import pool_wrapper
from thorny_core.db import event, UserFactory, GuildFactory


app = Sanic("thorny_server_app")


@app.route('/')
async def test(request: Request):
    return sanicjson({'hello': 'world'})


@app.post('/<gamertag:str>/connect')
async def connect(request: Request, gamertag: str):
    gamertag = gamertag[12:-3].replace("%20", " ")
    thorny_user = await UserFactory.build(client.get_user(await UserFactory.get_user_by_gamertag(gamertag)))
    thorny_guild = await GuildFactory.build(client.get_guild(thorny_user.guild_id))
    connection = event.Connect(client, datetime.now(), thorny_user, thorny_guild)
    await connection.log()
    return sanicjson({"Accept": True})


@app.post('/<gamertag:str>/disconnect')
async def disconnect(request: Request, gamertag: str):
    gamertag = gamertag[12:-3].replace("%20", " ")
    thorny_user = await UserFactory.build(client.get_user(await UserFactory.get_user_by_gamertag(gamertag)))
    thorny_guild = await GuildFactory.build(client.get_guild(thorny_user.guild_id))
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
async def start_bot(application):
    print("starting bot...")
    asyncio.get_event_loop().create_task(coro=client.start(TOKEN),
                                         name="Thorny Discord Client")

    await pool_wrapper.init_pool()

app.run(host="0.0.0.0")
