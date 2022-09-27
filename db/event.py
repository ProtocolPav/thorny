import random
import asyncpg as pg
from datetime import datetime, timedelta
import giphy_client
import json
import discord
from thorny_core import errors
from thorny_core.db import User, commit
from thorny_core.db import GuildFactory

config = json.load(open('../../thorny_data/config.json', 'r+'))
api_instance = giphy_client.DefaultApi()
giphy_token = config["giphy_token"]


class Event:
    def __init__(self, client: discord.Client, connection_pool: pg.Pool, event_time: datetime, user: User):
        self.client = client
        self.pool = connection_pool
        self.time = event_time
        self.thorny_user = user

    async def log(self):
        ...


class ConnectEvent(Event):
    async def log(self):
        async with self.pool.acquire() as conn:
            recent_connection = self.thorny_user.playtime.recent_connection

            if recent_connection is None or recent_connection['disconnect_time'] is not None:
                await conn.execute("""
                                   INSERT INTO thorny.activity(thorny_user_id, connect_time) 
                                   VALUES($1, $2)
                                   """,
                                   self.thorny_user.thorny_id, self.time)
                database_log = True
            elif datetime.now() - recent_connection['connect_time'] > timedelta(hours=12):
                playtime = timedelta(hours=1, minutes=5)
                await conn.execute("""
                                   UPDATE thorny.activity SET disconnect_time = $1, playtime = $2 
                                   WHERE thorny_user_id = $3 and connect_time = $4
                                   """,
                                   self.time, playtime, self.thorny_user.thorny_id, recent_connection['connect_time'])

                await conn.execute("""
                                   INSERT INTO thorny.activity(thorny_user_id, connect_time) 
                                   VALUES($1, $2)
                                   """,
                                   self.thorny_user.thorny_id, self.time)
                database_log = True
            else:
                database_log = False
            print(f"[{datetime.now().replace(microsecond=0)}] [CONNECT] ThornyID {self.thorny_user.thorny_id}")

        log_embed = discord.Embed(title=f'CONNECTION', colour=0x44ef56)
        log_embed.set_footer(text=f"Event Time: {self.time}")
        log_embed.set_author(name=self.thorny_user.username, icon_url=self.thorny_user.discord_member.display_avatar.url)

        thorny_guild = await GuildFactory.build(self.thorny_user.discord_member.guild)
        if thorny_guild.channels.logs_channel is not None:
            activity_channel = self.client.get_channel(thorny_guild.channels.logs_channel)
            await activity_channel.send(embed=log_embed)

        return database_log


class DisconnectEvent(Event):
    async def log(self):
        async with self.pool.acquire() as conn:
            recent_connection = self.thorny_user.playtime.recent_connection
            playtime_overtime = False

            if recent_connection is None or recent_connection['disconnect_time'] is not None:
                database_log = False
            else:
                playtime = self.time - recent_connection['connect_time']

                if playtime > timedelta(hours=12):
                    playtime_overtime = True
                    playtime = timedelta(hours=1, minutes=5)

                await conn.execute("""
                                   UPDATE thorny.activity SET disconnect_time = $1, playtime = $2, description = $5
                                   WHERE thorny_user_id = $3 and connect_time = $4
                                   """,
                                   self.time, playtime, self.thorny_user.thorny_id, recent_connection['connect_time'])

                database_log = True

            print(f"[{datetime.now().replace(microsecond=0)}] [DISCONNECT] ThornyID {self.thorny_user.thorny_id}")

        log_embed = discord.Embed(title=f'DISCONNECTION', colour=0xA52A2A)
        log_embed.set_footer(text=f"Event Time: {self.time}")
        log_embed.set_author(name=self.thorny_user.username,
                             icon_url=self.thorny_user.discord_member.display_avatar.url)

        thorny_guild = await GuildFactory.build(self.thorny_user.discord_member.guild)
        if thorny_guild.channels.logs_channel is not None:
            activity_channel = self.client.get_channel(thorny_guild.channels.logs_channel)
            await activity_channel.send(embed=log_embed)

        return database_log, playtime_overtime

