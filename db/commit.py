import json
from datetime import datetime

from thorny_core.db.user import User, InventorySlot, Strike
from thorny_core.db.guild import Guild


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


async def update_inventory_slot(thorny_user: User, inventory_slot: InventorySlot):
    async with thorny_user.connection_pool.connection() as conn:
        await conn.execute("""
                           UPDATE thorny.inventory
                           SET item_id = $1, item_count = $2
                           WHERE inventory_id = $3
                           """,
                           inventory_slot.item_id, inventory_slot.item_count, inventory_slot.inventory_id)


async def insert_inventory_slot(thorny_user: User, inventory_slot: InventorySlot):
    async with thorny_user.connection_pool.connection() as conn:
        await conn.execute("""
                           INSERT INTO thorny.inventory(thorny_user_id, item_id, item_count)
                           VALUES($1, $2, $3)
                           """,
                           thorny_user.thorny_id, inventory_slot.item_id, inventory_slot.item_count)


async def delete_inventory_slot(thorny_user: User, inventory_slot: InventorySlot):
    async with thorny_user.connection_pool.connection() as conn:
        await conn.execute("""
                           DELETE FROM thorny.inventory
                           WHERE inventory_id = $1
                           """,
                           inventory_slot.inventory_id)


async def insert_strike(thorny_user: User, strike: Strike):
    async with thorny_user.connection_pool.connection() as conn:
        await conn.execute("""
                           INSERT INTO thorny.strikes(thorny_user_id, manager_id, reason)
                           VALUES($1, $2, $3)
                           """,
                           strike.strike_id, strike.manager_id, strike.reason)


async def delete_strike(thorny_user: User, strike: Strike):
    async with thorny_user.connection_pool.connection() as conn:
        await conn.execute("""
                           DELETE FROM thorny.strikes
                           WHERE strike_id = $1
                           """,
                           strike.strike_id)


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
        await conn.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
        await conn.execute("""
                           UPDATE thorny.guild
                           SET channels = $1
                           WHERE guild_id = $2
                           """,
                           {"logs": thorny_guild.channels.logs_channel,
                            "welcome": thorny_guild.channels.welcome_channel,
                            "gulag": thorny_guild.channels.gulag_channel,
                            "projects": thorny_guild.channels.projects_channel,
                            "announcements": thorny_guild.channels.announcements_channel,
                            "thorny_updates": thorny_guild.channels.thorny_updates_channel},
                           thorny_guild.guild_id)


async def commit(object_to_commit: User | Guild):
    async with object_to_commit.connection_pool.connection() as conn:

        async with conn.transaction():
            if type(object_to_commit) == User:
                await update_user(object_to_commit)
                await update_profile(object_to_commit)
                await update_levels(object_to_commit)
                await update_counters(object_to_commit)

                original_slots = object_to_commit.inventory.original_slots
                slots = object_to_commit.inventory.slots
                if len(original_slots) > len(slots):
                    for slot in original_slots:
                        if slot not in slots:
                            await delete_inventory_slot(object_to_commit, slot)
                elif len(slots) > len(original_slots):
                    for slot in slots:
                        if slot not in original_slots:
                            await insert_inventory_slot(object_to_commit, slot)
                elif len(slots) == len(original_slots):
                    for slot in slots:
                        await update_inventory_slot(object_to_commit, slot)

                original_strikes = object_to_commit.strikes.original_strikes
                strikes = object_to_commit.strikes.strikes
                if len(original_strikes) > len(strikes):
                    for strike in original_strikes:
                        if strike not in strikes:
                            await delete_strike(object_to_commit, strike)
                elif len(strikes) > len(original_strikes):
                    for strike in strikes:
                        if strike not in original_strikes:
                            await insert_strike(object_to_commit, strike)

                print(f"[{datetime.now().replace(microsecond=0)}] [DATABASE] Committed ThornyUser with "
                      f"Thorny ID", object_to_commit.thorny_id)

            elif type(object_to_commit) == Guild:
                await update_guild(object_to_commit)
                await update_channels(object_to_commit)

                print(f"[{datetime.now().replace(microsecond=0)}] [DATABASE] Committed Guild {object_to_commit.guild_name} with "
                      f"ID", object_to_commit.guild_id)
