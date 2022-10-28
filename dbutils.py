import asyncpg
from datetime import datetime, timedelta

import discord

from db import UserFactory, pool
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


class Leaderboard:
    """This is needed"""
    def __init__(self):
        self.user_rank = None
        self.activity_list = None
        self.nugs_list = None
        self.treasury_list = None
        self.levels_list = None

    async def select_activity(self, thorny_user: user.User, month: datetime):
        async with pool.acquire() as conn:
            if datetime.now() < month:
                month = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - relativedelta(years=1)
            else:
                month = month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            next_month = month + relativedelta(months=1)
            self.activity_list = await conn.fetch(f"""
                                                  SELECT SUM(playtime), thorny.user.thorny_user_id, thorny.user.user_id
                                                  FROM thorny.activity 
                                                  JOIN thorny.user
                                                  ON thorny.user.thorny_user_id = thorny.activity.thorny_user_id
                                                  WHERE connect_time BETWEEN $1 AND $2
                                                  AND playtime IS NOT NULL
                                                  AND thorny.user.guild_id = $3 
                                                  AND thorny.user.active = True
                                                  GROUP BY thorny.user.user_id, thorny.user.thorny_user_id
                                                  ORDER BY SUM(playtime) DESC
                                                  """,
                                                  month, next_month, thorny_user.guild_id)
            for user in self.activity_list:
                if user['thorny_user_id'] == thorny_user.thorny_id:
                    self.user_rank = self.activity_list.index(user) + 1

    async def select_nugs(self, ctx):
        async with pool.acquire() as conn:
            self.nugs_list = await conn.fetch(f"SELECT user_id, thorny_user_id, balance FROM thorny.user "
                                              f"WHERE thorny.user.guild_id = $1 "
                                              f"AND thorny.user.active = True "
                                              f"GROUP BY user_id, thorny_user_id, balance "
                                              f"ORDER BY balance DESC", ctx.guild.id)
            thorny_user = await UserFactory.build(ctx.author)
            for user in self.nugs_list:
                if user['thorny_user_id'] == thorny_user.thorny_id:
                    self.user_rank = self.nugs_list.index(user) + 1

    async def select_treasury(self):
        async with pool.acquire() as conn:
            self.treasury_list = await conn.fetch(f"SELECT kingdom, treasury FROM thorny.kingdoms "
                                                  f"ORDER BY treasury DESC")

    async def select_levels(self, ctx, member: discord.Member = None):
        async with pool.acquire() as conn:
            self.levels_list = await conn.fetch("""
                                                SELECT thorny.user.user_id, thorny.levels.thorny_user_id, user_level
                                                FROM thorny.user 
                                                JOIN thorny.levels 
                                                ON thorny.user.thorny_user_id = thorny.levels.thorny_user_id
                                                WHERE thorny.user.guild_id = $1 
                                                AND thorny.user.active = True
                                                GROUP BY thorny.levels.thorny_user_id,
                                                thorny.user.user_id, user_level, xp
                                                ORDER BY xp DESC
                                                """,
                                                ctx.guild.id)
            if member is None:
                thorny_user = await UserFactory.build(ctx.author)
            else:
                thorny_user = await UserFactory.build(member)
            for user in self.levels_list:
                if user['thorny_user_id'] == thorny_user.thorny_id:
                    self.user_rank = self.levels_list.index(user) + 1


class User:
    """I could probably change this, but it is needed"""
    def __init__(self):
        self.list = None

    async def select_birthdays(self):
        async with pool.acquire() as conn:
            self.list = await conn.fetch("""SELECT user_id, birthday, guild_id
                                            FROM thorny.user
                                            WHERE active = True AND birthday IS NOT NULL""")
            return self.list


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
