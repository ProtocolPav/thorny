import random
import asyncpg as pg
from datetime import datetime, timedelta
import giphy_client
import json
import discord
from thorny_core import errors
from thorny_core.uikit import embeds
from thorny_core.db import User, Guild
from thorny_core.db import commit


config = json.load(open('../thorny_data/config.json', 'r+'))
api_instance = giphy_client.DefaultApi()
giphy_token = config["giphy_token"]


class Event:
    def __init__(self, client: discord.Client, event_time: datetime, user: User, guild: Guild):
        self.client = client
        self.time = event_time
        self.thorny_user = user
        self.thorny_guild = guild

    async def log(self):
        ...


class ConnectEvent(Event):
    async def log(self):
        async with self.thorny_user.connection_pool.acquire() as conn:
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

        if self.thorny_guild.channels.logs_channel is not None:
            activity_channel = self.client.get_channel(self.thorny_guild.channels.logs_channel)
            await activity_channel.send(embed=log_embed)

        return database_log


class DisconnectEvent(Event):
    async def log(self):
        async with self.thorny_user.connection_pool.acquire() as conn:
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

        if self.thorny_guild.channels.logs_channel is not None:
            activity_channel = self.client.get_channel(self.thorny_guild.channels.logs_channel)
            await activity_channel.send(embed=log_embed)

        return database_log, playtime_overtime


class GainXP(Event):
    def __init__(self, client: discord.Client, event_time: datetime, user: User, guild: Guild, message: discord.Message):
        super().__init__(client, event_time, user, guild)

        self.message = message

    async def log(self):
        level_up = False

        if self.time - self.thorny_user.counters.level_last_message > timedelta(minutes=1):
            self.thorny_user.level.xp += random.randint(5 * self.thorny_guild.xp_multiplier,
                                                        16 * self.thorny_guild.xp_multiplier)
            self.thorny_user.counters.level_last_message = self.time

            while self.thorny_user.level.xp > self.thorny_user.level.required_xp:
                self.thorny_user.level.level += 1
                lv = self.thorny_user.level.level
                self.thorny_user.level.required_xp += (lv ** 2) * 4 + (50 * lv) + 100

                level_up = True

            await commit(self.thorny_user)

        if level_up:
            await self.message.channel.send(embed=embeds.level_up_embed(self.thorny_user, self.thorny_guild))
