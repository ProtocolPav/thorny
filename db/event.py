import json
import random
from datetime import datetime, timedelta

import discord
import giphy_client

from thorny_core import errors
from thorny_core.db import User, Guild, commit
from thorny_core.uikit import embeds

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


class Connect(Event):
    async def log(self):
        async with self.thorny_user.connection_pool.connection() as conn:
            loose_connections = self.thorny_user.playtime.loose_connections

            if not loose_connections:
                await conn.execute("""
                                   INSERT INTO thorny.playtime(thorny_user_id, connect_time) 
                                   VALUES($1, $2)
                                   """,
                                   self.thorny_user.thorny_id, self.time)

                print(f"[{datetime.now().replace(microsecond=0)}] [CONNECT] ThornyID {self.thorny_user.thorny_id}")

                if self.thorny_guild.channels.get_channel('logs'):
                    activity_channel = self.client.get_channel(self.thorny_guild.channels.get_channel('logs'))
                    await activity_channel.send(embed=embeds.connect_embed(self.time, self.thorny_user))

            else:
                raise errors.AlreadyConnectedError()


class Disconnect(Event):
    def __init__(self, client: discord.Client, event_time: datetime, user: User, guild: Guild):
        super().__init__(client, event_time, user, guild)
        self.playtime: timedelta = timedelta(hours=0)
        self.playtime_overtime = False

    async def log(self):
        async with self.thorny_user.connection_pool.connection() as conn:
            loose_connections = self.thorny_user.playtime.loose_connections

            if not loose_connections:
                raise errors.NotConnectedError()
            else:
                self.playtime = self.time.replace(microsecond=0) - loose_connections[0]['connect_time'].replace(microsecond=0)

                await conn.execute("""
                                   UPDATE thorny.playtime SET disconnect_time = $1, playtime = $2
                                   WHERE playtime_id = $3
                                   """,
                                   self.time, self.playtime,
                                   loose_connections[0]['playtime_id'])

                print(f"[{datetime.now().replace(microsecond=0)}] [DISCONNECT] ThornyID {self.thorny_user.thorny_id}")

                if self.thorny_guild.channels.get_channel('logs'):
                    activity_channel = self.client.get_channel(self.thorny_guild.channels.get_channel('logs'))
                    await activity_channel.send(embed=embeds.disconnect_embed(self.time, self.thorny_user))


class AdjustPlaytime(Event):
    def __init__(self, client: discord.Client, event_time: datetime, user: User, guild: Guild, hour: int, minute: int):
        super().__init__(client, event_time, user, guild)
        self.hour = hour
        self.minute = minute

    async def log(self):
        async with self.thorny_user.connection_pool.connection() as conn:
            current_connection = self.thorny_user.playtime.current_connection

            if current_connection is None or current_connection['disconnect_time'] is None:
                raise errors.AlreadyConnectedError()

            else:
                playtime = current_connection['playtime'] - timedelta(hours=self.hour or 0, minutes=self.minute or 0)
                desc = f"Adjusted by {self.hour or 0}h{self.minute or 0}m | {current_connection['description']}"
                await conn.execute("""
                                   UPDATE thorny.activity SET playtime = $1, description = $2
                                   WHERE thorny_user_id = $3 and connect_time = $4
                                   """,
                                   playtime, desc, self.thorny_user.thorny_id, current_connection['connect_time'])


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


class Transaction(Event):
    def __init__(self, client: discord.Client, event_time: datetime, user: User, guild: Guild,
                 receivable: User, amount: int, reason: str):
        super().__init__(client, event_time, user, guild)

        self.receivable_user = receivable
        self.amount = amount
        self.reason = reason

    async def log(self):
        if self.thorny_guild.channels.get_channel('logs'):
            logs_channel = self.client.get_channel(self.thorny_guild.channels.get_channel('logs'))
            await logs_channel.send(embed=embeds.payment_log(self.thorny_user, self.receivable_user, self.thorny_guild,
                                                             self.amount, self.reason))

class Birthday(Event):
    async def log(self):
        if str(self.thorny_user.age)[-1] == "1":
            suffix = "st"
        elif str(self.thorny_user.age)[-1] == "2":
            suffix = "nd"
        elif str(self.thorny_user.age)[-1] == "3":
            suffix = "rd"
        else:
            suffix = "th"

        birthday_message = f"Wohoo!! It is {self.thorny_user.discord_member.mention}'s {self.thorny_user.age}{suffix} birthday " \
                           f"today! Happy Birthday, {self.thorny_user.username}! :partying_face: :partying_face: :partying_face:"

        if self.thorny_guild.channels.get_channel('welcome'):
            logs_channel = self.client.get_channel(self.thorny_guild.channels.get_channel('welcome'))
            await logs_channel.send(birthday_message)

