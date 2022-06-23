import asyncpg
import asyncpg as pg
import asyncio
from datetime import datetime, timedelta

import discord

from connection_pool import pool
from dbfactory import ThornyFactory
from dateutil.relativedelta import relativedelta


class Base:
    def __init__(self):
        self.returned = None

    async def select(self, item, table, where_condition=None, condition_is=None):
        async with pool.pool.acquire() as conn:
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
        async with pool.pool.acquire() as conn:
            self.returned = await conn.fetch("SELECT thorny.user.user_id, gamertag FROM thorny.profile "
                                             "JOIN thorny.user "
                                             "ON thorny.user.thorny_user_id = thorny.profile.thorny_user_id "
                                             "WHERE LOWER(gamertag) LIKE $1 "
                                             "AND thorny.user.guild_id = $2", f'%{gamertag[0:3].lower()}%', guild_id)
            return self.returned

    async def select_online(self, guild_id):
        async with pool.pool.acquire() as conn:
            self.returned = await conn.fetch("SELECT * FROM thorny.activity "
                                             "JOIN thorny.user "
                                             "ON thorny.user.thorny_user_id = thorny.activity.thorny_user_id "
                                             "WHERE disconnect_time is NULL AND connect_time > $1 "
                                             "AND thorny.user.guild_id = $2"
                                             "ORDER BY connect_time DESC", datetime.now().replace(day=1),
                                             guild_id)
            return self.returned

    async def update(self, item, item_new_value, table, where_condition=None, condition_is=None):
        self.returned = None  # just to make it a method
        async with pool.pool.acquire() as conn:
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
    def __init__(self):
        self.user_rank = None
        self.activity_list = None
        self.nugs_list = None
        self.treasury_list = None
        self.levels_list = None

    async def select_activity(self, ctx, month: datetime):
        async with pool.pool.acquire() as conn:
            if datetime.now() < month:
                month = month.replace(day=1) - relativedelta(years=1, days=1)
            else:
                month = month.replace(day=1) - relativedelta(days=1)
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
                                                  month, next_month, ctx.guild.id)
            thorny_user = await ThornyFactory.build(ctx.author)
            for user in self.activity_list:
                if user['thorny_user_id'] == thorny_user.id:
                    self.user_rank = self.activity_list.index(user) + 1

    async def select_nugs(self, ctx):
        async with pool.pool.acquire() as conn:
            self.nugs_list = await conn.fetch(f"SELECT user_id, thorny_user_id, balance FROM thorny.user "
                                              f"WHERE thorny.user.guild_id = $1 "
                                              f"AND thorny.user.active = True "
                                              f"GROUP BY user_id, thorny_user_id, balance "
                                              f"ORDER BY balance DESC", ctx.guild.id)
            thorny_user = await ThornyFactory.build(ctx.author)
            for user in self.nugs_list:
                if user['thorny_user_id'] == thorny_user.id:
                    self.user_rank = self.nugs_list.index(user) + 1

    async def select_treasury(self):
        async with pool.pool.acquire() as conn:
            self.treasury_list = await conn.fetch(f"SELECT kingdom, treasury FROM thorny.kingdoms "
                                                  f"ORDER BY treasury DESC")

    async def select_levels(self, ctx, member: discord.Member = None):
        async with pool.pool.acquire() as conn:
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
                thorny_user = await ThornyFactory.build(ctx.author)
            else:
                thorny_user = await ThornyFactory.build(member)
            for user in self.levels_list:
                if user['thorny_user_id'] == thorny_user.id:
                    self.user_rank = self.levels_list.index(user) + 1


class Kingdom:
    @staticmethod
    async def select_kingdom(kingdom):
        async with pool.pool.acquire() as conn:
            kingdom_dict = await conn.fetchrow("SELECT * "
                                               "FROM thorny.kingdoms "
                                               "WHERE kingdom = $1", kingdom)
            return kingdom_dict

    @staticmethod
    async def update_kingdom(kingdom, section, value):
        async with pool.pool.acquire() as conn:
            try:
                await conn.execute('UPDATE thorny.kingdoms '
                                   f'SET {section} = $1 '
                                   f'WHERE kingdom = $2', value, kingdom)
            except asyncpg.StringDataRightTruncationError:
                return "length_error"


class User:
    def __init__(self):
        self.list = None

    async def select_birthdays(self):
        async with pool.pool.acquire() as conn:
            self.list = await conn.fetch("""SELECT user_id, birthday, guild_id
                                            FROM thorny.user
                                            WHERE active = True AND birthday IS NOT NULL""")
            return self.list


class Update:
    @staticmethod
    async def update_v1_7_4():
        async with pool.pool.acquire() as conn:
            await conn.execute("""
                                CREATE TABLE thorny.guilds (
                                guild_id int8,
                                welcome_channel_id int8,
                                logs_channel_id int8,
                                xp_gain bool,
                                timeout_role_id int8,
                                timeout_channel_id int8,
                                thorny_update_channel_id int8,
                                PRIMARY KEY(guild_id))""")


"""Select Online Members
Get User Kingdom
Update item type

Select Statements
Update statements"""
