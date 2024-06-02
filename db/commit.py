import json
from datetime import datetime

from thorny_core.db.user import User
from thorny_core.db.guild import Guild
from thorny_core.db.project import Project


async def update_user(thorny_user: User):
    async with thorny_user.connection_pool.connection() as conn:
        await conn.execute("""
                           UPDATE thorny.user
                           SET username = $1, balance = $2, join_date = $3, birthday = $4
                           WHERE thorny_user_id = $5
                           """,
                           thorny_user.username, thorny_user.balance, thorny_user.join_date.time,
                           thorny_user.birthday.time, thorny_user.thorny_id)


async def update_profile(thorny_user: User):
    profile = thorny_user.profile
    async with thorny_user.connection_pool.connection() as conn:
        await conn.execute("""
                           UPDATE thorny.profile
                           SET slogan = $1, gamertag = $2, aboutme = $3, lore = $4, 
                           character_name = $5, character_age = $6, character_race = $7,
                           character_role = $8, character_origin = $9, character_beliefs = $10,
                           agility = $11, valor = $12, strength = $13, charisma = $14, 
                           creativity = $15, ingenuity = $16, whitelisted_gamertag = $17
                           WHERE thorny_user_id = $18
                           """,
                           profile.slogan, profile.gamertag, profile.aboutme, profile.lore,
                           profile.character_name, profile.character_age, profile.character_race,
                           profile.character_role, profile.character_origin, profile.character_beliefs,
                           profile.agility, profile.valor, profile.strength,
                           profile.charisma, profile.creativity, profile.ingenuity, profile.whitelisted_gamertag,
                           thorny_user.thorny_id)


async def update_levels(thorny_user: User):
    async with thorny_user.connection_pool.connection() as conn:
        await conn.execute("""
                           UPDATE thorny.levels
                           SET user_level = $1, xp = $2, required_xp = $3
                           WHERE thorny_user_id = $4
                           """,
                           thorny_user.level.level, thorny_user.level.xp, thorny_user.level.required_xp,
                           thorny_user.thorny_id)


async def update_counters(thorny_user: User):
    counters = thorny_user.counters
    async with thorny_user.connection_pool.connection() as conn:
        await conn.execute("""
                           UPDATE thorny.counter
                           SET count = $1
                           WHERE counter_name = 'ticket_count' AND thorny_user_id = $2
                           """,
                           counters.ticket_count, thorny_user.thorny_id)
        await conn.execute("""
                           UPDATE thorny.counter
                           SET datetime = $1
                           WHERE counter_name = 'ticket_last_purchase' AND thorny_user_id = $2
                           """,
                           counters.ticket_last_purchase, thorny_user.thorny_id)
        await conn.execute("""
                           UPDATE thorny.counter
                           SET datetime = $1
                           WHERE counter_name = 'level_last_message' AND thorny_user_id = $2
                           """,
                           counters.level_last_message, thorny_user.thorny_id)


async def update_guild(thorny_guild: Guild):
    async with thorny_guild.connection_pool.connection() as conn:
        await conn.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
        await conn.execute("""
                           UPDATE thorny.guild
                           SET currency_name = $1, currency_emoji = $2, 
                           level_up_message = $3, join_message = $4, leave_message = $5, xp_multiplier = $6, enable_levels = $7
                           WHERE guild_id = $8
                           """,
                           thorny_guild.currency.name,
                           thorny_guild.currency.emoji, thorny_guild.level_message, thorny_guild.join_message,
                           thorny_guild.leave_message, float(thorny_guild.xp_multiplier), thorny_guild.levels_enabled,
                           thorny_guild.guild_id)


async def update_channels(thorny_guild: Guild):
    async with thorny_guild.connection_pool.connection() as conn:
        for channel in thorny_guild.channels.all_channels():
            await conn.execute("""
                               UPDATE thorny.channels
                               SET channel_id = $1
                               WHERE guild_id = $2 AND channel_type = $3
                               """,
                               channel['channel_id'], thorny_guild.guild_id, channel['channel_type'])


async def update_project(project: Project):
    async with project.connection_pool.connection() as conn:
        await conn.execute("""
                           UPDATE thorny.projects
                           SET status = $1, name = $2, thread_id = $3, coordinates = $4,
                           description = $5, time_estimation = $6, road_built = $7, members = $8,
                           progress = $9, accepted_on = $10, completed_on = $11
                           WHERE project_id = $12
                           """,
                           project.status, project.name, project.thread_id, project.coordinates, project.description,
                           project.time_estimation, project.road_built, project.members, project.progress, project.accept_date,
                           project.complete_date,
                           project.project_id)


async def commit(object_to_commit: User | Guild | Project):
    """
    Commit an object to the database. This saves the object's files in the database. Currently you can only commit
    ThornyUser, Guild and Project objects.
    --------
    Parameters:
        object_to_commit: ThornyUser or Guild or Project
    """
    async with object_to_commit.connection_pool.connection() as conn:

        async with conn.transaction():
            if type(object_to_commit) == User:
                await update_user(object_to_commit)
                await update_profile(object_to_commit)
                await update_levels(object_to_commit)
                await update_counters(object_to_commit)

                print(f"[{datetime.now().replace(microsecond=0)}] [DATABASE] Committed ThornyUser with "
                      f"Thorny ID", object_to_commit.thorny_id)

            elif type(object_to_commit) == Guild:
                await update_guild(object_to_commit)
                await update_channels(object_to_commit)

                print(f"[{datetime.now().replace(microsecond=0)}] [DATABASE] Committed Guild {object_to_commit.guild_name} with "
                      f"ID", object_to_commit.guild_id)

            elif type(object_to_commit) == Project:
                await update_project(object_to_commit)

                print(f"[{datetime.now().replace(microsecond=0)}] [DATABASE] Committed Project {object_to_commit.name} with "
                      f"ID", object_to_commit.project_id)
