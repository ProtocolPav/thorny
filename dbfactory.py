import asyncpg as pg
from datetime import datetime, timedelta
import discord
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass
from connection_pool import pool
from dbclass import ThornyUser

from discord.utils import get


class ThornyFactory:
    @classmethod
    async def build(cls, member: discord.Member):
        async with pool.acquire() as conn:
            user_id = member.id
            guild_id = member.guild.id
            now = datetime.now()
            thorny_user = await conn.fetchrow("""SELECT * FROM thorny.user
                                                 WHERE user_id = $1 AND guild_id = $2""", user_id, guild_id)
            thorny_id = thorny_user['thorny_user_id']

            current_month = now.replace(day=1, hour=0, minute=0)
            previous_month = now.replace(day=1, hour=0, minute=0) - relativedelta(months=1)
            expiring_month = now.replace(day=1, hour=0, minute=0) - relativedelta(months=2)

            user_profile = await conn.fetchrow("""SELECT * FROM thorny.profile
                                                  INNER JOIN thorny.levels
                                                  ON thorny.levels.thorny_user_id = thorny.profile.thorny_user_id
                                                  WHERE thorny.profile.thorny_user_id = $1""", thorny_id)
            profile_column_data = await conn.fetch("""
                                                        SELECT column_name, data_type, character_maximum_length
                                                        FROM INFORMATION_SCHEMA.COLUMNS
                                                        WHERE TABLE_SCHEMA = 'thorny' AND TABLE_NAME   = 'profile'
                                                      """)
            user_activity = await conn.fetchrow("""SELECT * FROM thorny.user_activity
                                                   WHERE thorny_user_id = $1""", thorny_id)
            user_playtime_stats = await conn.fetchrow("""SELECT SUM(playtime) as total_playtime, 
                                                         SUM(case when connect_time
                                                         between $3 and $2 then playtime end) as current_playtime,
                                                         SUM(case when connect_time
                                                         between $4 and $3 then playtime end) as previous_playtime,
                                                         SUM(case when connect_time
                                                         between $5 and $4 then playtime end) as expiring_playtime
                                                         FROM thorny.activity
                                                         WHERE thorny_user_id = $1
                                                         GROUP BY thorny_user_id""",
                                                      thorny_id, now, current_month, previous_month, expiring_month)
            user_daily_average = await conn.fetchrow("""SELECT thorny_user_id, AVG(sums) as averages FROM
                                                        (SELECT thorny_user_id, DATE(connect_time), SUM(playtime) AS sums
                                                        FROM thorny.activity 
                                                        GROUP BY thorny_user_id, DATE(connect_time)) AS query
                                                        WHERE thorny_user_id = 1
                                                        GROUP BY thorny_user_id""")
            user_recent_playtime = await conn.fetchrow("""SELECT playtime FROM thorny.activity
                                                          WHERE thorny_user_id = $1 AND disconnect_time IS NOT NULL
                                                          ORDER BY connect_time DESC""", thorny_id)
            user_strikes = await conn.fetch("""SELECT * from thorny.strikes
                                               WHERE thorny_user_id = $1""", thorny_id)
            user_inventory = await conn.fetch("""
                                                SELECT * FROM thorny.inventory
                                                INNER JOIN thorny.item_type ON 
                                                thorny.item_type.friendly_id = thorny.inventory.item_id
                                                WHERE thorny.inventory.thorny_user_id = $1
                                              """, thorny_id)
            item_data = await conn.fetch("""
                                            SELECT * FROM thorny.item_type
                                         """)
            user_counters = await conn.fetch("""SELECT * from thorny.counter
                                                WHERE thorny_user_id = $1""", thorny_id)

            master_datalayer = DataLayer(discord_member=member,
                                         connection_pool=pool,
                                         thorny_user=thorny_user,
                                         profile=user_profile,
                                         column_data=profile_column_data,
                                         playtime=user_activity,
                                         playtime_stats=user_playtime_stats,
                                         daily_average=user_daily_average,
                                         recent_playtime=user_recent_playtime,
                                         strikes=user_strikes,
                                         inventory=user_inventory,
                                         item_data=item_data,
                                         counters=user_counters)
            return ThornyUser(master_datalayer)

    @classmethod
    async def create(cls, member_list: list[discord.Member]):
        async with pool.acquire() as conn:
            for member in member_list:
                if not member.bot:
                    user_id = member.id
                    guild_id = member.guild.id
                    user = await conn.fetchrow("""SELECT * FROM thorny.user
                                                  WHERE user_id = $1 AND guild_id = $2""", user_id, guild_id)
                    if user is None:
                        await conn.execute("""INSERT INTO thorny.user(user_id, guild_id, join_date, balance, username)
                                              VALUES($1, $2, $3, $4, $5)""",
                                           user_id, guild_id, member.joined_at, 25, member.name)
                        thorny_id = await conn.fetchrow("""SELECT thorny_user_id FROM thorny.user
                                                           WHERE user_id=$1 AND guild_id=$2""", user_id, guild_id)
                        await conn.execute("""INSERT INTO thorny.user_activity(thorny_user_id)
                                              VALUES($1)""", thorny_id[0])
                        await conn.execute("""INSERT INTO thorny.profile(thorny_user_id)
                                              VALUES($1)""", thorny_id[0])
                        await conn.execute("""INSERT INTO thorny.levels(thorny_user_id)
                                              VALUES($1)""", thorny_id[0])
                        await conn.execute("""INSERT INTO thorny.counter(thorny_user_id, counter_name, count)
                                              VALUES($1, $2, $3)""", thorny_id[0], 'ticket_count', 0)
                        await conn.execute("""INSERT INTO thorny.counter(thorny_user_id, counter_name, datetime)
                                              VALUES($1, $2, $3)""", thorny_id[0], 'ticket_last_purchase', datetime.now())
                        await conn.execute("""INSERT INTO thorny.counter(thorny_user_id, counter_name, datetime)
                                              VALUES($1, $2, $3)""", thorny_id[0], 'level_last_message', datetime.now())
                        print("[SERVER] User profile created with Thorny ID", thorny_id[0])
                    else:
                        await conn.execute("""UPDATE thorny.user
                                              SET active = True WHERE thorny_user_id = $1""", user['thorny_user_id'])
                        print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] Reactivated account of "
                              f"{user['username']}, Thorny ID {user['thorny_user_id']}")

    @classmethod
    async def deactivate(cls, member_list: list[discord.Member]):
        async with pool.acquire() as conn:
            for member in member_list:
                if not member.bot:
                    thorny_user = await conn.fetchrow("""SELECT * FROM thorny.user
                                                         WHERE user_id = $1 AND guild_id = $2""",
                                                      member.id, member.guild.id)
                    thorny_id = thorny_user['thorny_user_id']
                    await conn.execute("""UPDATE thorny.user
                                          SET active = False WHERE thorny_user_id = $1""",
                                       thorny_id)
                    print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] Deactivated account of "
                          f"{thorny_user['username']}, Thorny ID {thorny_id}")


@dataclass
class DataLayer:
    discord_member: discord.Member
    connection_pool: pg.Pool
    thorny_user: pg.Record
    profile: pg.Record
    column_data: pg.Record
    playtime: pg.Record
    playtime_stats: pg.Record
    daily_average: pg.Record
    recent_playtime: pg.Record
    strikes: pg.Record
    inventory: pg.Record
    item_data: pg.Record
    counters: pg.Record
