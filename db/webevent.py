from datetime import datetime

import asyncpg as pg
import discord

from thorny_core.db import UserFactory, GuildFactory, event, poolwrapper
from thorny_core import errors


class WebEvent:
    __pool: poolwrapper.PoolWrapper
    __client: discord.Client
    id: int
    time: datetime
    event: str
    description: str
    processed: bool
    process_time: datetime

    def __init__(self, event_rec: pg.Record, pool: poolwrapper.PoolWrapper, client: discord.Client):
        self.__pool = pool
        self.__client = client
        self.id = event_rec['event_id']
        self.time = event_rec['event_time']
        self.event = event_rec['event']
        self.description = event_rec['description']
        self.processed = event_rec['processed']
        self.process_time = event_rec['processed_time']

    async def mark_successful_processing(self):
        async with self.__pool.connection() as conn:
            self.processed = True
            self.process_time = datetime.now()
            await conn.execute("""
                               UPDATE webserver.webevent
                               SET processed = True, processed_time = $2
                               WHERE event_id = $1
                               """,
                               self.id, self.process_time)

            print(f"[PROCESSING] Successfully processed a {self.event} with ID {self.id}")

    async def mark_failed_processing(self):
        async with self.__pool.connection() as conn:
            self.processed = False
            self.process_time = datetime.now()
            await conn.execute("""
                               UPDATE webserver.webevent
                               SET processed = NULL
                               WHERE event_id = $1
                               """,
                               self.id)

            print(f"[PROCESSING] Failed to process a {self.event} with ID {self.id}")

    async def process(self):
        if not self.processed:
            if self.event.lower() in ['connect', 'disconnect']:
                event_type = event.Connect if self.event.lower() == 'connect' else event.Disconnect

                guild_id = int(self.description.split(',')[0])
                gamertag = self.description.split(',')[1]

                thorny_guild = await GuildFactory.build(self.__client.get_guild(guild_id))

                discord_member = thorny_guild.discord_guild.get_member(await UserFactory.get_user_by_gamertag(gamertag, guild_id))
                thorny_user = await UserFactory.build(discord_member)

                connection = event_type(client=self.__client,
                                        event_time=self.time,
                                        user=thorny_user,
                                        guild=thorny_guild)

                try:
                    await connection.log()
                    await self.mark_successful_processing()
                except errors.AlreadyConnectedError:
                    await self.mark_failed_processing()
                except errors.NotConnectedError:
                    raise errors.NotConnectedError()

            elif self.event.lower() == 'disconnect all':
                guild_id = int(self.description)
                thorny_guild = await GuildFactory.build(self.__client.get_guild(guild_id))

                for connected_user in await thorny_guild.get_online_players():
                    thorny_user = await UserFactory.build(thorny_guild.discord_guild.get_member(connected_user['user_id']))
                    disconnection = event.Disconnect(self.__client, self.time, thorny_user, thorny_guild)
                    await disconnection.log()

                await self.mark_successful_processing()

async def fetch_pending_webevents(pool: poolwrapper.PoolWrapper, client: discord.Client) -> list[WebEvent]:
    async with pool.connection() as conn:
        return_list = []
        unprocessed_events = await conn.fetch("""
                                              SELECT * FROM webserver.webevent
                                              WHERE processed = False
                                              ORDER BY event_time ASC
                                              """)

        for pending_event in unprocessed_events:
            return_list.append(WebEvent(pending_event,
                                        pool,
                                        client))

    return return_list