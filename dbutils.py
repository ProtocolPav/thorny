import asyncpg
from datetime import datetime, timedelta

import discord

from db.poolwrapper import pool_wrapper
from db import user
from dateutil.relativedelta import relativedelta


class Base:
    def __init__(self):
        self.returned = None

    async def select(self, item, table, where_condition=None, condition_is=None):
        async with pool_wrapper.connection() as conn:
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
        async with pool_wrapper.connection() as conn:
            self.returned = await conn.fetch("SELECT thorny.user.user_id, gamertag FROM thorny.profile "
                                             "JOIN thorny.user "
                                             "ON thorny.user.thorny_user_id = thorny.profile.thorny_user_id "
                                             "WHERE LOWER(gamertag) LIKE $1 "
                                             "AND thorny.user.guild_id = $2", f'%{gamertag[0:3].lower()}%', guild_id)
            return self.returned

