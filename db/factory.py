import asyncio
import json
from datetime import datetime
from typing import Literal

import discord
from discord import User as DiscordUser, Member as DiscordMember
import httpx
from dateutil.relativedelta import relativedelta

from thorny_core.db.guild import Guild
from thorny_core.db.user import User
from thorny_core.db.project import Project
from thorny_core.db.commit import commit
from thorny_core.db.poolwrapper import pool_wrapper
from thorny_core import errors


class UserFactory:
    @classmethod
    async def build(cls, member: DiscordMember | DiscordUser) -> User:
        """
        Build a User class based on the Discord Member object.
        This is used when you know who the person is, e.g. In an application command where `ctx.user` is available
        """
        async with pool_wrapper.connection() as conn:
            user_id = member.id
            guild_id = member.guild.id
            thorny_user = await conn.fetchrow("""
                                              SELECT * FROM thorny.user
                                              WHERE user_id = $1 AND guild_id = $2
                                              """,
                                              user_id, guild_id)
            if not thorny_user:
                await UserFactory.create([member])

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

            monthly_playtime = await conn.fetch("""
                                                SELECT t.year, t.month, sum(t.playtime) as playtime
                                                FROM (SELECT sum(playtime) as playtime, 
                                                             date_part('month', connect_time) as month, 
                                                             date_part('year', connect_time) as year
                                                      FROM thorny.playtime
                                                      INNER JOIN thorny.user 
                                                        ON thorny.playtime.thorny_user_id = thorny.user.thorny_user_id 
                                                      WHERE thorny.playtime.thorny_user_id = $1
                                                      GROUP BY connect_time 
                                                      ) as t
                                                GROUP BY t.year, t.month
                                                ORDER BY t.year DESC, t.month DESC
                                                """,
                                                thorny_id)

            playtime_stats = await conn.fetchrow("""
                                                 SELECT SUM(playtime) as total_playtime,
                                                        SUM(case when date(connect_time) = date(now()) then playtime end) as today
                                                 FROM thorny.playtime
                                                 WHERE thorny_user_id = $1
                                                 GROUP BY thorny_user_id
                                                 """,
                                                 thorny_id)

            daily_playtime = await conn.fetch("""
                                              SELECT t.day, sum(t.playtime) as playtime 
                                              FROM (SELECT sum(playtime) as playtime, 
                                                           date(connect_time) as day
                                                    FROM thorny.playtime
                                                    INNER JOIN thorny.user
                                                        ON thorny.playtime.thorny_user_id = thorny.user.thorny_user_id 
                                                    WHERE thorny.playtime.thorny_user_id = $1
                                                    GROUP BY day 
                                                    ) as t
                                              GROUP BY t.day
                                              ORDER BY t.day desc
                                              """,
                                              thorny_id)

            current_connection = await conn.fetchrow("""
                                                     SELECT * FROM thorny.playtime
                                                     WHERE thorny_user_id = $1
                                                     ORDER BY connect_time DESC
                                                     """,
                                                     thorny_id)

            unfulfilled_connections = await conn.fetch("""
                                                       SELECT * FROM thorny.playtime
                                                       WHERE thorny_user_id = $1 AND disconnect_time is NULL
                                                       ORDER BY connect_time ASC
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
            return User(pool=pool_wrapper,
                        member=member,
                        thorny_user=thorny_user,
                        thorny_guild=await GuildFactory.build(member.guild),
                        profile=profile,
                        profile_columns=profile_column_data,
                        levels=levels,
                        monthly_playtime=monthly_playtime,
                        daily_playtime=daily_playtime,
                        total_playtime=playtime_stats,
                        current_connection=current_connection,
                        unfulfilled_connections=unfulfilled_connections,
                        inventory=inventory,
                        item_data=item_data,
                        strikes=strikes,
                        counters=counters)

    @classmethod
    async def fetch_by_id(cls, guild: Guild, thorny_id: int) -> User:
        """
        Fetch a User object based on the ThornyID of the user. This requires you also knowing the Guild the user is in.
        --------
        Parameters:
        guild: Guild
        thorny_id: int
        """
        async with pool_wrapper.connection() as conn:
            thorny_user = await conn.fetchrow("""
                                              SELECT user_id FROM thorny.user
                                              WHERE thorny_user_id = $1
                                              """,
                                              thorny_id)
            member = guild.discord_guild.get_member(thorny_user['user_id'])
        return await UserFactory.build(member)

    @classmethod
    async def fetch_by_gamertag(cls, guild: Guild, gamertag: str) -> User:
        """
        Fetch a User object based on the gamertag of the user. This requires you to know the Guild the user is in.
        --------
        Parameters:
        guild: Guild
        gamertag: str
        """
        async with pool_wrapper.connection() as conn:
            thorny_user = await conn.fetchrow("""
                                              SELECT thorny.user.user_id FROM thorny.user
                                              INNER JOIN thorny.profile
                                              ON thorny.user.thorny_user_id = thorny.profile.thorny_user_id
                                              WHERE whitelisted_gamertag = $1
                                              """,
                                              gamertag)
            member = guild.discord_guild.get_member(thorny_user['user_id'])
        return await UserFactory.build(member)

    @classmethod
    async def create(cls, members: list[discord.Member]):
        """
        Create or re-activate a new User object in the database. This does not return the User object.

        Creating a User: If a new user joins a guild, it will create a new ThornyID for them
        Re-Activating a User: If a user left and re-joined the guild, it will activate the ThornyID account

        This should only be used in Thorny Events. If you need to create a User and return it, use `UserFactory.build()` instead
        --------
        Parameters:
        members: list[discord.Member]
        """
        async with pool_wrapper.connection() as conn:
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
        """
        Deactivates the account of a user. Only use when the user leaves a guild.
        --------
        Parameters:
        members: list[discord.Member]
        """
        async with pool_wrapper.connection() as conn:
            for member in members:
                thorny_user = await UserFactory.build(member)

                if thorny_user.profile.whitelisted_gamertag is not None:
                    async with httpx.AsyncClient() as client:
                        r: httpx.Response = await client.get("http://thorny-bds:8000/status", timeout=None)

                        if r.json()['server_online']:
                            removed_gamertag = thorny_user.profile.whitelisted_gamertag
                            thorny_user.profile.whitelisted_gamertag = None
                            await commit(thorny_user)

                            await client.post(f"http://thorny-bds:8000/<gamertag:{removed_gamertag}>/whitelist/remove")

                await conn.execute("""
                                   UPDATE thorny.user
                                   SET active = False WHERE thorny_user_id = $1
                                   """,
                                   thorny_user.thorny_id)
                print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] Deactivated account of "
                      f"{thorny_user.username}, Thorny ID {thorny_user.thorny_id}")

    @classmethod
    async def get_gamertags(cls, guild_id: int, gamertag: str = None):
        """
        Leave gamertag blank to get all gamertags in the database.

        Checks for gamertags that are similar. Use part of a gamertag to get all similar ones.
        E.g. gamertag='Prot' will get all the gamertags similar to prot
        """
        async with pool_wrapper.connection() as conn:
            if gamertag is None:
                returned = await conn.fetch("""
                                            SELECT thorny.user.user_id, whitelisted_gamertag
                                            FROM thorny.profile
                                            JOIN thorny.user ON thorny.user.thorny_user_id = thorny.profile.thorny_user_id
                                            WHERE thorny.user.guild_id = $1 AND whitelisted_gamertag is not NULL
                                            """,
                                            guild_id)
            else:
                returned = await conn.fetch("""
                                            SELECT thorny.user.user_id, whitelisted_gamertag FROM thorny.profile
                                            INNER JOIN thorny.user
                                            ON thorny.user.thorny_user_id = thorny.profile.thorny_user_id
                                            WHERE LOWER(whitelisted_gamertag) LIKE $1
                                            AND thorny.user.guild_id = $2
                                            """,
                                            f'%{gamertag}%', guild_id)
            return returned


class GuildFactory:
    FEATURES = Literal['EVERTHORN', 'LEVELS', 'BETA', 'PROFILE', 'PLAYTIME', 'ROA']

    @classmethod
    async def build(cls, guild: discord.Guild) -> Guild:
        async with pool_wrapper.connection() as conn:
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

            features = await conn.fetch("""
                                        SELECT * FROM thorny.guild_feature
                                        WHERE guild_id = $1
                                        """,
                                        guild.id)
            all_features = await conn.fetch("""
                                            SELECT * FROM thorny.feature
                                            WHERE configured = true
                                            """)

            responses = await conn.fetch("""
                                         SELECT * FROM thorny.responses
                                         WHERE guild_id = $1
                                         """,
                                         guild.id)

            channels = await conn.fetch("""
                                        SELECT * FROM thorny.channels
                                        WHERE guild_id = $1
                                        """,
                                        guild.id)

            return Guild(pool=pool_wrapper,
                         guild=guild,
                         guild_record=guild_rec,
                         channels_record=channels,
                         features_record=features,
                         responses_record=responses,
                         reaction_roles=reaction_roles,
                         currency_total=total_currency['total'])

    @classmethod
    async def create(cls, guild: discord.Guild):
        async with pool_wrapper.connection() as conn:
            default_features = ['BASIC', 'PROFILE', 'PLAYTIME', 'LEVELS']

            guild_exists = await conn.fetchrow("""
                                               SELECT guild_id FROM thorny.guild
                                               WHERE guild_id = $1
                                               """,
                                               guild.id)

            if guild_exists is None:
                await conn.execute("""
                                   INSERT INTO thorny.guild(guild_id, guild_name)
                                   VALUES ($1, $2)
                                   """,
                                   guild.id, guild.name
                                   )
                for feature in default_features:
                    await conn.execute("""
                                       INSERT INTO thorny.guild_feature
                                       VALUES ($1, $2)
                                       """,
                                       guild.id, feature.upper()
                                       )

                await conn.execute("""
                                   INSERT INTO thorny.responses
                                   VALUES ($1, $2, $3, $4)
                                   """,
                                   guild.id, 'exact', 'response', "You've just triggered my super secret response!"
                                   )

                print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] Created guild "
                      f"{guild.name}, ID {guild.id}")

            else:
                await conn.execute("""
                                   UPDATE thorny.guild
                                   SET active = True WHERE guild_id = $1
                                   """,
                                   guild.id)

                print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] Reactivated guild "
                      f"{guild.name}, ID {guild.id}")

    @classmethod
    async def deactivate(cls, guild: discord.Guild):
        async with pool_wrapper.connection() as conn:
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
            async with pool_wrapper.connection() as conn:
                guild_ids = await conn.fetch("""
                                             SELECT thorny.guild_feature.guild_id FROM thorny.guild_feature
                                             INNER JOIN thorny.guild ON thorny.guild.guild_id = thorny.guild_feature.guild_id
                                             WHERE feature = $1
                                             AND active = True
                                             """,
                                             feature.upper())

                return [i['guild_id'] for i in guild_ids]

        return asyncio.get_event_loop().run_until_complete(get())

    @classmethod
    def check_guild_feature(cls, guild: Guild, feature: FEATURES):
        if feature not in guild.features:
            raise errors.AccessDenied(feature)


class ProjectFactory:
    @classmethod
    async def build(cls, project_id: int, owner: User) -> Project:
        async with pool_wrapper.connection() as conn:
            project_data = await conn.fetchrow("""
                                               SELECT * FROM thorny.projects
                                               WHERE project_id = $1
                                               """,
                                               project_id)

            project_updates = ...

            return Project(pool_wrapper=pool_wrapper, project_data=project_data, owner=owner)

    @classmethod
    async def fetch_by_user(cls, thorny_user: User) -> list[Project]:
        async with pool_wrapper.connection() as conn:
            project_ids = await conn.fetch("""
                                           SELECT project_id FROM thorny.projects
                                           WHERE owner_id = $1 AND status != $2
                                           """,
                                           thorny_user.thorny_id, "building application")

            project_list = []
            for project_id in project_ids:
                project_list.append(await ProjectFactory.build(project_id[0], thorny_user))

            return project_list

    @classmethod
    async def fetch_by_thread(cls, thread_id: int, thorny_guild: Guild) -> Project:
        async with pool_wrapper.connection() as conn:
            project_id = await conn.fetchrow("""
                                             SELECT owner_id, project_id FROM thorny.projects
                                             WHERE thread_id = $1
                                             """,
                                             thread_id)

            if project_id is None:
                raise ...

            thorny_user = await UserFactory.fetch_by_id(thorny_guild, project_id['owner_id'])

            return await ProjectFactory.build(project_id['project_id'], thorny_user)

    @classmethod
    async def create(cls, thorny_user: User) -> Project:
        async with pool_wrapper.connection() as conn:
            in_construction = await conn.fetchrow("""
                                                  SELECT project_id FROM thorny.projects
                                                  WHERE owner_id = $1 AND status = $2
                                                  """,
                                                  thorny_user.thorny_id, "building application")

            if in_construction:
                return await ProjectFactory.build(in_construction[0], thorny_user)

            else:
                await conn.execute("""
                                   INSERT INTO thorny.projects(owner_id, status)
                                   VALUES($1, $2)
                                   """,
                                   thorny_user.thorny_id, "building application")

                project_id = await conn.fetchrow("""
                                                 SELECT project_id FROM thorny.projects
                                                 WHERE owner_id = $1 AND status = $2
                                                 """,
                                                 thorny_user.thorny_id, "building application")

                return await ProjectFactory.build(project_id[0], thorny_user)
