import sys

import sanic.log
from sanic import Sanic, Request
from sanic.response import json as sanicjson
from datetime import datetime
import asyncio

from thorny import thorny as client, TOKEN
from thorny_core.db.poolwrapper import pool_wrapper
from thorny_core.db import event, UserFactory, GuildFactory


log_config = dict(  # no cov
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": "INFO", "handlers": ["console"]},
        "sanic.error": {
            "level": "INFO",
            "handlers": ["info_rotating_file_handler"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["info_rotating_file_handler"],
            "propagate": True,
            "qualname": "sanic.access",
        },
        "sanic.server": {
            "level": "INFO",
            "handlers": ["info_rotating_file_handler"],
            "propagate": True,
            "qualname": "sanic.server",
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout,
        },
        'info_rotating_file_handler': {
            'level': 'INFO',
            'formatter': 'generic',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'sanic.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        }
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
            + "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
)

app = Sanic("thorny-bot-app", log_config=log_config)


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
async def start_bot(application: Sanic, loop: asyncio.AbstractEventLoop):
    await client.login(TOKEN)
    await application.add_task(client.connect(reconnect=True), name="Thorny Discord Client")
    # asyncio.get_event_loop().create_task(coro=client.connect(reconnect=True),
    #                                      name="Thorny Discord Client")

    # birthday_checker.start()
    # day_counter.start()
    # interruption_check.start()

    await pool_wrapper.init_pool()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, single_process=True)
