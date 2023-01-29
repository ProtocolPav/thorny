import asyncpg
from datetime import datetime, timedelta

import discord

from db import pool
from db import user
from dateutil.relativedelta import relativedelta


class Base:
    def __init__(self):
        self.returned = None

    async def select(self, item, table, where_condition=None, condition_is=None):
        async with pool.acquire() as conn:
            if where_condition is not None:
                self.returned = await conn.fetch(f"""
                                                 SELECT {item} FROM thorny.{table}
                                                 WHERE {where_condition} = $1
                                                 """,
                                                 condition_is)
                return self.returned
            else:
                self.returned = await conn.fetch(f"""
                                                 SELECT {item} FROM thorny.{table}
                                                 """)
                return self.returned

    async def select_gamertags(self, guild_id, gamertag):
        async with pool.acquire() as conn:
            self.returned = await conn.fetch("SELECT thorny.user.user_id, gamertag FROM thorny.profile "
                                             "JOIN thorny.user "
                                             "ON thorny.user.thorny_user_id = thorny.profile.thorny_user_id "
                                             "WHERE LOWER(gamertag) LIKE $1 "
                                             "AND thorny.user.guild_id = $2", f'%{gamertag[0:3].lower()}%', guild_id)
            return self.returned

    async def select_online(self, guild_id):
        async with pool.acquire() as conn:
            self.returned = await conn.fetch("SELECT * FROM thorny.activity "
                                             "JOIN thorny.user "
                                             "ON thorny.user.thorny_user_id = thorny.activity.thorny_user_id "
                                             "WHERE disconnect_time is NULL "
                                             "AND thorny.user.guild_id = $1"
                                             "ORDER BY connect_time DESC",
                                             guild_id)
            return self.returned

    async def update(self, item, item_new_value, table, where_condition=None, condition_is=None):
        self.returned = None  # just to make it a method
        async with pool.acquire() as conn:
            if where_condition is not None:
                await conn.execute(f"""
                                    UPDATE thorny.{table}
                                    SET {item} = $1
                                    WHERE {where_condition} = $2
                                    """,
                                   item_new_value, condition_is)
                return True
            elif where_condition is None:
                await conn.execute(f"""
                                    UPDATE thorny.{table}
                                    SET {item} = $1
                                    """,
                                   item_new_value)
                return True
            else:
                return False


class WebserverUpdates:
    @staticmethod
    async def connect(gamertag: str, event_time: datetime, connection):
        thorny_user = await connection.fetchrow("""
                                                SELECT thorny.user.thorny_user_id
                                                FROM thorny.profile
                                                INNER JOIN thorny.user ON 
                                                thorny.user.thorny_user_id = thorny.profile.thorny_user_id
                                                WHERE gamertag = $1
                                                AND thorny.user.guild_id = 611008530077712395
                                                """,
                                                gamertag)
        recent_connection = await connection.fetchrow("""
                                                      SELECT * FROM thorny.activity
                                                      WHERE thorny_user_id = $1
                                                      ORDER BY connect_time DESC
                                                      """,
                                                      thorny_user[0])
        if recent_connection['disconnect_time'] is None:
            playtime = event_time - recent_connection['connect_time']
            await connection.execute("""
                                     UPDATE thorny.activity SET disconnect_time = $1, playtime = $2, description = $5
                                     WHERE thorny_user_id = $3 and connect_time = $4
                                     """,
                                     event_time, playtime, thorny_user[0], recent_connection['connect_time'],
                                     'Automatic Disconnect')
            print(f"[{event_time}] [DISCONNECT] {gamertag}, with Thorny ID {thorny_user[0]} has disconnected")

        await connection.execute("""
                                 INSERT INTO thorny.activity(thorny_user_id, connect_time) 
                                 VALUES($1, $2)
                                 """,
                                 thorny_user[0], event_time)
        print(f"[{event_time}] [CONNECT] {gamertag}, with Thorny ID {thorny_user[0]} has connected to Everthorn")

    @staticmethod
    async def disconnect(gamertag: str, event_time: datetime, connection):
        thorny_user = await connection.fetchrow("""
                                                SELECT thorny.user.thorny_user_id
                                                FROM thorny.profile
                                                INNER JOIN thorny.user ON 
                                                thorny.user.thorny_user_id = thorny.profile.thorny_user_id
                                                WHERE gamertag = $1
                                                AND thorny.user.guild_id = 611008530077712395
                                                """,
                                                gamertag)
        recent_connection = await connection.fetchrow("""
                                                      SELECT * FROM thorny.activity
                                                      WHERE thorny_user_id = $1
                                                      ORDER BY connect_time DESC
                                                      """,
                                                      thorny_user[0])
        playtime = event_time - recent_connection['connect_time']
        await connection.execute("""
                                 UPDATE thorny.activity SET disconnect_time = $1, playtime = $2, description = $5
                                 WHERE thorny_user_id = $3 and connect_time = $4
                                 """,
                                 event_time, playtime, thorny_user[0], recent_connection['connect_time'],
                                 'Automatic Disconnect')
        print(f"[{event_time}] [DISCONNECT] {gamertag}, with Thorny ID {thorny_user[0]} has disconnected")

    @staticmethod
    async def disconnect_all(guild_id: int, event_time: datetime):
        async with pool.acquire() as connection:
            all_online = await Base().select_online(guild_id)

            for person in all_online:
                recent_connection = await connection.fetchrow("""
                                                              SELECT * FROM thorny.activity
                                                              WHERE thorny_user_id = $1
                                                              ORDER BY connect_time DESC
                                                              """,
                                                              person['thorny_user_id'])

                playtime = event_time - recent_connection['connect_time']
                await connection.execute("""
                                         UPDATE thorny.activity SET disconnect_time = $1, playtime = $2, description = $5
                                         WHERE thorny_user_id = $3 and connect_time = $4
                                         """,
                                         event_time, playtime, person['thorny_user_id'], recent_connection['connect_time'],
                                         'Disconnect All')
                print(f"[{event_time}] [DISCONNECT ALL] User with Thorny ID {person['thorny_user_id']} has disconnected")

