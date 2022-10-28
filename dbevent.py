import random
import asyncpg as pg
from datetime import datetime, timedelta
import giphy_client
import json
import discord
import errors
from dataclasses import dataclass
from db import User, commit
from thorny_core.db import GuildFactory

api_instance = giphy_client.DefaultApi()
giphy_token = "PYTVyPc9klW4Ej3ClWz9XFCo1TQOp72b"

# TODO change the entire Events classes


@dataclass
class EventMetadata:
    """
    Always initialize the Event Metadata, and then pass it on to the Event Class as needed
    """

    user: User
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

    sender_user: User = None
    receiver_user: User = None
    nugs_amount: int = None

    level_up: bool = False
    xp_multiplier: int = 1
    xp_gained: int = 0
    level_up_message = None

    message_before: discord.Message = None
    message_after: discord.Message = None
    deleted_message: discord.Message = None


class Event:
    def __init__(self, metadata: EventMetadata):
        self.metadata = metadata
        self.time = metadata.event_time
        self.user = metadata.user
        self.pool = metadata.pool
        self.client = metadata.client
        self.config = json.load(open("../thorny_data/config.json", "r"))

    async def log_event_in_database(self):
        """
        Every class must have this method, but it is different for each.
        The Database Log must always be run first, and depending on the boolean value of database_log,
        the Discord Log will be run.
        """

    async def log_event_in_discord(self):
        """
        Every class must have this method, but it is different for each
        """

    def edit_metadata(self, attribute, new_val):
        self.metadata.__setattr__(attribute, new_val)


class ConnectEvent(Event):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.recent_connection = metadata.recent_connection

    async def log_event_in_discord(self):
        log_embed = discord.Embed(title=f'CONNECTION', colour=0x44ef56)
        log_embed.set_footer(text=f"Event Time: {self.time}")
        log_embed.set_author(name=self.user.username, icon_url=self.user.discord_member.display_avatar.url)
        activity_channel = self.client.get_channel(self.config['channels']['activity_logs'])
        await activity_channel.send(embed=log_embed)

    async def log_event_in_database(self):
        data = self.metadata
        async with self.pool.acquire() as conn:
            if self.recent_connection is None or self.recent_connection['disconnect_time'] is not None:
                await conn.execute("""
                                   INSERT INTO thorny.activity(thorny_user_id, connect_time) 
                                   VALUES($1, $2)
                                   """,
                                   self.user.thorny_id, self.time)
                data.database_log = True
            elif datetime.now() - self.recent_connection['connect_time'] > timedelta(hours=12):
                playtime = timedelta(hours=1, minutes=5)
                await conn.execute("""
                                   UPDATE thorny.activity SET disconnect_time = $1, playtime = $2 
                                   WHERE thorny_user_id = $3 and connect_time = $4
                                   """,
                                   self.time, playtime, self.user.thorny_id, self.recent_connection['connect_time'])

                await conn.execute("""
                                   INSERT INTO thorny.activity(thorny_user_id, connect_time) 
                                   VALUES($1, $2)
                                   """,
                                   self.user.thorny_id, self.time)
                data.database_log = True
                data.playtime_overtime = True
                data.playtime = playtime
            print(f"[{datetime.now().replace(microsecond=0)}] [CONNECT] ThornyID {self.user.thorny_id}")
            return data


class DisconnectEvent(Event):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.recent_connection = metadata.recent_connection

    async def log_event_in_discord(self):
        log_embed = discord.Embed(title=f'DISCONNECTION', colour=0x44ef56)
        log_embed.set_footer(text=f"Event Time: {self.time}")
        log_embed.set_author(name=self.user.username, icon_url=self.user.discord_member.display_avatar.url)
        activity_channel = self.client.get_channel(self.config['channels']['activity_logs'])
        await activity_channel.send(embed=log_embed)

    async def log_event_in_database(self):
        data = self.metadata
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
                                   self.time, playtime, self.user.thorny_id, self.recent_connection['connect_time'],
                                   data.event_comment)
                data.database_log = True
                data.playtime = playtime
            print(f"[{datetime.now().replace(microsecond=0)}] [DISCONNECT] ThornyID {self.user.thorny_id}")
            return data


class AdjustEvent(Event):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.recent_connection = metadata.recent_connection

    async def log_event_in_discord(self):
        log_embed = discord.Embed(title=f'PLAYTIME ADJUSTED', colour=0x44ef56)
        log_embed.set_footer(text=f"Event Time: {self.time}")
        log_embed.set_author(name=self.user.username, icon_url=self.user.discord_member.display_avatar.url)
        activity_channel = self.client.get_channel(self.config['channels']['activity_logs'])
        await activity_channel.send(embed=log_embed)

    async def log_event_in_database(self):
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
                                   playtime, desc, self.user.thorny_id, self.recent_connection['connect_time'])
                self.metadata.database_log = True
        return self.metadata


class PlayerTransaction(Event):
    def __init__(self, metadata):
        super().__init__(metadata)

    async def log_event_in_database(self):
        """
        I will need to add this function later when I create the logs table in the database
        """

    async def log_event_in_discord(self):
        data = self.metadata

        log_embed = discord.Embed(color=0xF4C430)
        log_embed.add_field(name="**Transaction**",
                            value=f"<@{data.sender_user.thorny_id}> paid <@{data.receiver_user.thorny_id}> "
                                  f"**<:Nug:884320353202081833>{data.nugs_amount}**\n"
                                  f"Reason: {data.event_comment}")
        log_embed.set_footer(text=f"Event Time: {self.time}")
        logs_channel = self.client.get_channel(self.config['channels']['event_logs'])
        await logs_channel.send(embed=log_embed)


class StoreTransaction(Event):
    def __init__(self, metadata):
        super().__init__(metadata)

    async def log_event_in_database(self):
        """
        I will need to add this function later when I create the logs table in the database
        """

    async def log_event_in_discord(self):
        data = self.metadata

        log_embed = discord.Embed(color=0xF4C430)
        log_embed.add_field(name="**Transaction**",
                            value=f"<@{data.sender_user.thorny_id}> paid the Store "
                                  f"**<:Nug:884320353202081833>{data.nugs_amount}**\n"
                                  f"Reason: {data.event_comment}")
        log_embed.set_footer(text=f"Event Time: {self.time}")
        logs_channel = self.client.get_channel(self.config['channels']['event_logs'])
        await logs_channel.send(embed=log_embed)


class Birthday(Event):
    def __init__(self, metadata):
        super().__init__(metadata)

    async def log_event_in_database(self):
        user = self.metadata.user
        try:
            user.inventory.add_item("gift", 1)
        except errors.ItemMaxCountError:
            pass
        await commit(user)

    async def log_event_in_discord(self):
        user = self.metadata.user
        birthday = user.birthday

        age = datetime.now().year - birthday.time.year
        if str(age)[-1] == "1":
            suffix = "st"
        elif str(age)[-1] == "2":
            suffix = "nd"
        elif str(age)[-1] == "3":
            suffix = "rd"
        else:
            suffix = "th"

        birthday_message = f"Wohoo!! It is {user.discord_member.mention}'s {age}{suffix} birthday today! " \
                           f"Happy Birthday, {user.username}! :partying_face: :partying_face: :partying_face: "

        thorny_guild = await GuildFactory.build(self.metadata.user.discord_member.guild)
        if thorny_guild.channels.welcome_channel is not None:
            logs_channel = self.client.get_channel(thorny_guild.channels.welcome_channel)
            await logs_channel.send(birthday_message)


async def fetch(event, thorny_user: User, client, metadata: EventMetadata = None):
    if metadata is None:
        metadata = EventMetadata(thorny_user, client, thorny_user.connection_pool,
                                 datetime.now().replace(microsecond=0))
    async with thorny_user.connection_pool.acquire() as connection:
        metadata.recent_connection = await connection.fetchrow("""
                                                               SELECT * FROM thorny.activity
                                                               WHERE thorny_user_id = $1
                                                               ORDER BY connect_time DESC
                                                               """,
                                                               thorny_user.thorny_id)
        return event(metadata)
