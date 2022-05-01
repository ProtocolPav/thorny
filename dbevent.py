import asyncpg
import random
import asyncpg as pg
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
import discord
import errors
from dataclasses import dataclass, field
from dbclass import ThornyUser
from dbcommit import commit
from connection_pool import pool
import math


@dataclass
class EventMetadata:
    """
    Always initialize the Event Metadata, and then pass it on to the Event Class as needed
    """

    user: ThornyUser
    client: discord.Client
    pool: pg.Pool
    event_time: datetime
    database_log: bool = False
    event_comment: str = "None"

    playtime_overtime: bool = False
    playtime: timedelta = None
    recent_connection: pg.Record = None
    adjusting_hour = None
    adjusting_minute = None

    sender_user: ThornyUser = None
    receiver_user: ThornyUser = None
    nugs_amount: int = None

    level_up: bool = False


class Event:
    def __init__(self, metadata: EventMetadata):
        self.metadata = metadata
        self.time = metadata.event_time
        self.user = metadata.user
        self.pool = metadata.pool
        self.client = metadata.client
        self.config = json.load(open("../thorny_data/config.json", "r"))

    async def log_event_in_database(self) -> EventMetadata:
        """
        Every class must have this method, but it is different for each.
        The Database Log must always be run first, and depending on the boolean value of database_log,
        the Discord Log will be run.
        """

    async def log_event_in_discord(self):
        """
        Every class must have this method, but it is different for each
        """


class ConnectEvent(Event):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.recent_connection = metadata.recent_connection

    async def log_event_in_discord(self):
        log_embed = discord.Embed(title=f'CONNECTION', colour=0x44ef56)
        log_embed.set_footer(text=f"Event Time: `{self.time}`")
        log_embed.set_author(name=self.user.username, icon_url=self.user.member_object.display_avatar.url)
        activity_channel = self.client.get_channel(self.config['channels']['activity_logs'])
        await activity_channel.send(embed=log_embed)

    async def log_event_in_database(self) -> EventMetadata:
        data = self.metadata
        async with self.pool.acquire() as conn:
            if self.recent_connection is None or self.recent_connection['disconnect_time'] is not None:
                await conn.execute("""
                                   INSERT INTO thorny.activity(thorny_user_id, connect_time) 
                                   VALUES($1, $2)
                                   """,
                                   self.user.id, self.time)
                data.database_log = True
            elif datetime.now() - self.recent_connection['connect_time'] > timedelta(hours=12):
                playtime = timedelta(hours=1, minutes=5)
                await conn.execute("""
                                   UPDATE thorny.activity SET disconnect_time = $1, playtime = $2 
                                   WHERE thorny_user_id = $3 and connect_time = $4
                                   """,
                                   self.time, playtime, self.user.id, self.recent_connection['connect_time'])

                await conn.execute("""
                                   INSERT INTO thorny.activity(thorny_user_id, connect_time) 
                                   VALUES($1, $2)
                                   """,
                                   self.user.id, self.time)
                data.database_log = True
                data.playtime_overtime = True
                data.playtime = playtime
            return data


class DisconnectEvent(Event):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.recent_connection = metadata.recent_connection

    async def log_event_in_discord(self):
        log_embed = discord.Embed(title=f'DISCONNECTION', colour=0x44ef56)
        log_embed.set_footer(text=f"Event Time: `{self.time}`")
        log_embed.set_author(name=self.user.username, icon_url=self.user.member_object.display_avatar.url)
        activity_channel = self.client.get_channel(self.config['channels']['activity_logs'])
        await activity_channel.send(embed=log_embed)

    async def log_event_in_database(self) -> EventMetadata:
        data = self.metadata
        print(self.recent_connection)
        async with self.pool.acquire() as conn:
            if self.recent_connection is None or self.recent_connection['disconnect_time'] is not None:
                data.database_log = False
            else:
                playtime = self.time - self.recent_connection['connect_time']
                if playtime > timedelta(hours=12):
                    data.playtime_overtime = True
                    playtime = timedelta(hours=1, minutes=5)
                await conn.execute("""
                                   UPDATE thorny.activity SET disconnect_time = $1, playtime = $2, description = $5
                                   WHERE thorny_user_id = $3 and connect_time = $4
                                   """,
                                   self.time, playtime, self.user.id, self.recent_connection['connect_time'],
                                   data.event_comment)
                data.database_log = True
                data.playtime = playtime
            return data


class AdjustEvent(Event):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.recent_connection = metadata.recent_connection

    async def log_event_in_discord(self):
        log_embed = discord.Embed(title=f'PLAYTIME ADJUSTED', colour=0x44ef56)
        log_embed.set_footer(text=f"Event Time: `{self.time}`")
        log_embed.set_author(name=self.user.username, icon_url=self.user.member_object.display_avatar.url)
        activity_channel = self.client.get_channel(self.config['channels']['activity_logs'])
        await activity_channel.send(embed=log_embed)

    async def log_event_in_database(self) -> EventMetadata:
        async with self.pool.acquire() as conn:
            if self.recent_connection is None or self.recent_connection['disconnect_time'] is None:
                self.metadata.database_log = False
            else:
                hour = self.metadata.adjusting_hour
                minute = self.metadata.adjusting_minute
                playtime = self.recent_connection['playtime'] - timedelta(hours=hour or 0, minutes=minute or 0)
                desc = f"Adjusted by {hour or 0}h{minute or 0}m | {self.recent_connection['description']}"
                await conn.execute("""
                                    UPDATE thorny.activity SET playtime = $1, description = $2
                                    WHERE thorny_user_id = $3 and connect_time = $4
                                   """,
                                   playtime, desc, self.user.id, self.recent_connection['connect_time'])
                self.metadata.database_log = True
        return self.metadata


class PlayerTransaction(Event):
    def __init__(self, metadata):
        super().__init__(metadata)

    async def log_event_in_database(self) -> EventMetadata:
        """
        I will need to add this function later when I create the logs table in the database
        """

    async def log_event_in_discord(self):
        data = self.metadata

        log_embed = discord.Embed(color=0xF4C430)
        log_embed.add_field(name="**Transaction**",
                            value=f"<@{data.sender_user.id}> paid <@{data.receiver_user.id}> "
                                  f"**<:Nug:884320353202081833>{data.nugs_amount}**\n"
                                  f"Reason: {data.event_comment}")
        log_embed.set_footer(text=f"Event Time: `{self.time}`")
        logs_channel = self.client.get_channel(self.config['channels']['event_logs'])
        await logs_channel.send(embed=log_embed)


class StoreTransaction(Event):
    def __init__(self, metadata):
        super().__init__(metadata)

    async def log_event_in_database(self) -> EventMetadata:
        """
        I will need to add this function later when I create the logs table in the database
        """

    async def log_event_in_discord(self):
        data = self.metadata

        log_embed = discord.Embed(color=0xF4C430)
        log_embed.add_field(name="**Transaction**",
                            value=f"<@{data.sender_user.id}> paid the Store "
                                  f"**<:Nug:884320353202081833>{data.nugs_amount}**\n"
                                  f"Reason: {data.event_comment}")
        log_embed.set_footer(text=f"Event Time: `{self.time}`")
        logs_channel = self.client.get_channel(self.config['channels']['event_logs'])
        await logs_channel.send(embed=log_embed)


class GainXP(Event):
    def __init__(self, metadata):
        super().__init__(metadata)

    async def log_event_in_database(self) -> EventMetadata:
        thorny_user = self.metadata.user
        thorny_user.counters.level_last_message = datetime.now()
        thorny_user.profile.xp += random.randint(2, 14)
        if thorny_user.profile.xp >= thorny_user.profile.required_xp:
            thorny_user.profile.level += 1
            lv = thorny_user.profile.level
            thorny_user.profile.required_xp = (lv ** 2) * 4 + (60 * lv) + 100
            self.metadata.level_up = True
        await commit(thorny_user)
        self.metadata.user = thorny_user
        self.metadata.database_log = True
        return self.metadata

    async def log_event_in_discord(self):
        pass


async def fetch(event, thorny_user: ThornyUser, client, adjust_hour=None, adjust_minute=None):
    metadata = EventMetadata(thorny_user, client, thorny_user.pool, datetime.now().replace(microsecond=0))
    async with thorny_user.pool.acquire() as connection:
        metadata.recent_connection = await connection.fetchrow("""
                                                               SELECT * FROM thorny.activity
                                                               WHERE thorny_user_id = $1
                                                               ORDER BY connect_time DESC
                                                               """,
                                                               thorny_user.id)
        metadata.adjusting_hour = adjust_hour
        metadata.adjusting_minute = adjust_minute
        return event(metadata)
