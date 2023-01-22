import asyncpg as pg
import asyncio
import json
from datetime import datetime
import discord
from dateutil.relativedelta import relativedelta
from thorny_core.db.user import User
from thorny_core.db.guild import Guild
from typing import Literal


async def create_pool(loop=None):
    config = json.load(open('../thorny_data/config.json', 'r+'))
    pool_object = await pg.create_pool(database=config['database']['name'],
                                       user=config['database']['user'],
                                       password=config['database']['password'],
                                       host=config['database']['host'],
                                       port=5432,
                                       max_inactive_connection_lifetime=10.0,
                                       max_size=300,
                                       loop=loop)
    return pool_object


pool: pg.Pool = asyncio.get_event_loop().run_until_complete(create_pool())


class UserFactory:
    @classmethod
    async def build(cls, member: discord.Member) -> User:
        async with pool.acquire() as conn:
            user_id = member.id
            guild_id = member.guild.id
            thorny_user = await conn.fetchrow("""
                                              SELECT * FROM thorny.user
                                              WHERE user_id = $1 AND guild_id = $2
                                              """,
                                              user_id, guild_id)
            thorny_id = thorny_user['thorny_user_id']

            profile = await conn.fetchrow("""
                                          SELECT * FROM thorny.profile
                                          WHERE thorny_user_id = $1
                                          """,
                                          thorny_id)
            profile_column_data = await conn.fetch("""
                                                   SELECT column_name, data_type, character_maximum_length
                                                   FROM INFORMATION_SCHEMA.COLUMNS
                                                   WHERE TABLE_SCHEMA = 'thorny' AND TABLE_NAME = 'profile'
                                                   """)
            levels = await conn.fetchrow("""
                                         SELECT * FROM thorny.levels
                                         WHERE thorny_user_id = $1
                                         """,
                                         thorny_id)

            today = datetime.now()
            today_hour_zero = today.replace(hour=0, minute=0)
            current_month = today.replace(day=1, hour=0, minute=0)
            previous_month = today.replace(day=1, hour=0, minute=0) - relativedelta(months=1)
            expiring_month = today.replace(day=1, hour=0, minute=0) - relativedelta(months=2)

            playtime = await conn.fetchrow("""
                                           SELECT SUM(playtime)
                                           AS total_playtime,
                                           SUM(case when connect_time > $6 then playtime end)
                                           AS todays_playtime,
                                           SUM(case when connect_time between $3 and $2 then playtime end)
                                           AS current_playtime,
                                           SUM(case when connect_time between $4 and $3 then playtime end)
                                           AS previous_playtime,
                                           SUM(case when connect_time between $5 and $4 then playtime end)
                                           AS expiring_playtime
                                           FROM thorny.activity
                                           WHERE thorny_user_id = $1
                                           GROUP BY thorny_user_id
                                           """,
                                           thorny_id, today, current_month, previous_month, expiring_month,
                                           today_hour_zero)

            daily_average = await conn.fetchrow("""
                                                SELECT thorny_user_id, AVG(sums) AS averages 
                                                FROM (
                                                      SELECT thorny_user_id, DATE(connect_time), SUM(playtime)
                                                      AS sums
                                                      FROM thorny.activity 
                                                      GROUP BY thorny_user_id, DATE(connect_time)
                                                      ) AS query
                                                WHERE thorny_user_id = $1
                                                GROUP BY thorny_user_id
                                                """,
                                                thorny_id)
            recent_session = await conn.fetchrow("""
                                                 SELECT * FROM thorny.activity
                                                 WHERE thorny_user_id = $1 AND disconnect_time IS NOT NULL
                                                 ORDER BY connect_time DESC
                                                 """,
                                                 thorny_id)
            current_connection = await conn.fetchrow("""
                                                     SELECT * FROM thorny.activity
                                                     WHERE thorny_user_id = $1
                                                     ORDER BY connect_time DESC
                                                     """,
                                                     thorny_id)
            inventory = await conn.fetch("""
                                         SELECT * FROM thorny.inventory
                                         INNER JOIN thorny.item_type
                                         ON thorny.item_type.friendly_id = thorny.inventory.item_id
                                         WHERE thorny.inventory.thorny_user_id = $1
                                         """,
                                         thorny_id)
            item_data = await conn.fetch("""
                                         SELECT * FROM thorny.item_type
                                         """)
            strikes = await conn.fetch("""
                                       SELECT * from thorny.strikes
                                       WHERE thorny_user_id = $1
                                       """,
                                       thorny_id)
            counters = await conn.fetch("""
                                        SELECT * from thorny.counter
                                        WHERE thorny_user_id = $1
                                        """,
                                        thorny_id)
            return User(pool=pool,
                        member=member,
                        thorny_user=thorny_user,
                        profile=profile,
                        profile_columns=profile_column_data,
                        levels=levels,
                        playtime=playtime,
                        recent_playtime=recent_session,
                        current_connection=current_connection,
                        daily_average=daily_average,
                        inventory=inventory,
                        item_data=item_data,
                        strikes=strikes,
                        counters=counters)

    @classmethod
    async def get(cls, guild: discord.Guild, thorny_id: int) -> User:
        async with pool.acquire() as conn:
            thorny_user = await conn.fetchrow("""SELECT * FROM thorny.user
                                                 WHERE thorny_user_id = $1""", thorny_id)
            member = guild.get_member(thorny_user['user_id'])
        return await UserFactory.build(member)

    @classmethod
    async def create(cls, members: list[discord.Member]):
        async with pool.acquire() as conn:
            for member in members:
                user_id = member.id
                guild_id = member.guild.id
                user = await conn.fetchrow("""
                                           SELECT * FROM thorny.user
                                           WHERE user_id = $1 AND guild_id = $2
                                           """,
                                           user_id, guild_id)
                if user is None:
                    await conn.execute("""
                                       INSERT INTO thorny.user(user_id, guild_id, join_date, balance, username)
                                       VALUES($1, $2, $3, $4, $5)
                                       """,
                                       user_id, guild_id, member.joined_at, 25, member.name)
                    thorny_id = await conn.fetchrow("""
                                                    SELECT thorny_user_id FROM thorny.user
                                                    WHERE user_id=$1 AND guild_id=$2
                                                    """,
                                                    user_id, guild_id)
                    await conn.execute("""
                                       INSERT INTO thorny.profile(thorny_user_id)
                                       VALUES($1)
                                       """,
                                       thorny_id[0])
                    await conn.execute("""
                                       INSERT INTO thorny.levels(thorny_user_id)
                                       VALUES($1)
                                       """,
                                       thorny_id[0])
                    await conn.execute("""
                                       INSERT INTO thorny.counter(thorny_user_id, counter_name, count)
                                       VALUES($1, $2, $3)
                                       """,
                                       thorny_id[0], 'ticket_count', 0)
                    await conn.execute("""
                                       INSERT INTO thorny.counter(thorny_user_id, counter_name, datetime)
                                       VALUES($1, $2, $3)
                                       """,
                                       thorny_id[0], 'ticket_last_purchase', datetime.now())
                    await conn.execute("""
                                       INSERT INTO thorny.counter(thorny_user_id, counter_name, datetime)
                                       VALUES($1, $2, $3)
                                       """,
                                       thorny_id[0], 'level_last_message', datetime.now())
                    print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] User profile created with Thorny ID",
                          thorny_id[0])

                else:
                    await conn.execute("""
                                       UPDATE thorny.user
                                       SET active = True WHERE thorny_user_id = $1
                                       """,
                                       user['thorny_user_id'])
                    print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] Reactivated account of "
                          f"{user['username']}, Thorny ID {user['thorny_user_id']}")

    @classmethod
    async def deactivate(cls, members: list[discord.Member]):
        async with pool.acquire() as conn:
            for member in members:
                thorny_user = await conn.fetchrow("""
                                                  SELECT * FROM thorny.user
                                                  WHERE user_id = $1 AND guild_id = $2
                                                  """,
                                                  member.id, member.guild.id)
                thorny_id = thorny_user['thorny_user_id']
                await conn.execute("""
                                   UPDATE thorny.user
                                   SET active = False WHERE thorny_user_id = $1
                                   """,
                                   thorny_id)
                print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] Deactivated account of "
                      f"{thorny_user['username']}, Thorny ID {thorny_id}")

    @classmethod
    async def get_birthdays(cls):
        async with pool.acquire() as conn:
            bdays = await conn.fetch("""SELECT thorny_user_id, birthday, guild_id
                                        FROM thorny.user
                                        WHERE active = True AND birthday IS NOT NULL
                                        AND date_part('day', birthday) = date_part('day', now())
                                        AND date_part('month', birthday) = date_part('month', now())""")
            return bdays

    @classmethod
    async def get_user_by_gamertag(cls, gamertag):
        async with pool.acquire() as conn:
            user = await conn.fetchrow("""
                                       SELECT thorny.user.user_id FROM thorny.user
                                       INNER JOIN thorny.profile
                                       ON thorny.profile.thorny_user_id = thorny.user.thorny_user_id
                                       WHERE gamertag = $1
                                       """,
                                       gamertag)

            return user


class GuildFactory:
    FEATURES = Literal['BASIC', 'EVERTHORN', 'PREMIUM', 'BETA', 'PROFILE', 'PLAYTIME', 'ROA']

    @classmethod
    async def build(cls, guild: discord.Guild) -> Guild:
        async with pool.acquire() as conn:
            await conn.set_type_codec(
                'json',
                encoder=json.dumps,
                decoder=json.loads,
                schema='pg_catalog'
            )

            total_currency = await conn.fetchrow("""
                                                 SELECT SUM(balance) as total FROM thorny.user
                                                 WHERE guild_id = $1 AND active = TRUE
                                                 """,
                                                 guild.id)

            reaction_roles = await conn.fetch("""
                                              SELECT * FROM thorny.reactions
                                              WHERE guild_id = $1
                                              """,
                                              guild.id)

            guild_rec = await conn.fetchrow("""
                                            SELECT * FROM thorny.guild
                                            WHERE guild_id = $1
                                            """,
                                            guild.id)

            return Guild(pool=pool,
                         guild=guild,
                         guild_record=guild_rec,
                         reaction_roles=reaction_roles,
                         currency_total=total_currency['total'])

    @classmethod
    async def create(cls, guild: discord.Guild):
        async with pool.acquire() as conn:
            await conn.set_type_codec(
                'json',
                encoder=json.dumps,
                decoder=json.loads,
                schema='pg_catalog'
            )

            exact_default = {"secret": ["You've found my secret exact response!"]}
            wildcard_default = {"super secret": ["You've found my super secret wildcard response!"]}

            guild_exists = await conn.fetchrow("""
                                               SELECT guild_id FROM thorny.guild
                                               WHERE guild_id = $1
                                               """,
                                               guild.id)

            if guild_exists is None:
                await conn.execute("""
                                   INSERT INTO thorny.guild (guild_id, responses_exact, responses_wildcard)
                                   VALUES ($1, $2, $3)
                                   """,
                                   guild.id, exact_default, wildcard_default
                                   )
            print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] Created guild "
                  f"{guild.name}, ID {guild.id}")

    @classmethod
    async def deactivate(cls, guild: discord.Guild):
        async with pool.acquire() as conn:
            await conn.execute("""
                               UPDATE thorny.guild
                               SET active = False WHERE guild_id = $1
                               """,
                               guild.id)
            print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] Deactivated guild "
                  f"{guild.name}, ID {guild.id}")

    @classmethod
    def get_guilds_by_feature(cls, feature: FEATURES):
        async def get():
            async with pool.acquire() as conn:
                guild_ids = await conn.fetch("""
                                             SELECT guild_id FROM thorny.guild
                                             WHERE $1 = any(features_v2)
                                             AND active = True
                                             """,
                                             feature.upper())

                guilds = [i['guild_id'] for i in guild_ids]

                return guilds

        return asyncio.get_event_loop().run_until_complete(get())
