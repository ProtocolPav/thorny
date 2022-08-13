from datetime import datetime
from thorny_core.db.user import User, InventorySlot, Strike


async def update_user(thorny_user: User):
    async with thorny_user.connection_pool.acquire() as conn:
        await conn.execute("""
                           UPDATE thorny.user
                           SET username = $1, balance = $2, join_date = $3, birthday = $4
                           WHERE thorny_user_id = $5
                           """,
                           thorny_user.username, thorny_user.balance, thorny_user.join_date, thorny_user.birthday,
                           thorny_user.thorny_id)


async def update_profile(thorny_user: User):
    profile = thorny_user.profile
    async with thorny_user.connection_pool.acquire() as conn:
        await conn.execute("""
                           UPDATE thorny.profile
                           SET slogan = $1, gamertag = $2, aboutme = $3, lore = $4, role = $5,
                           aboutme_shown = $6, activity_shown = $7, lore_shown = $8
                           WHERE thorny_user_id = $9
                           """,
                           profile.slogan, profile.gamertag, profile.aboutme, profile.lore, profile.role,
                           profile.aboutme_shown, profile.activity_shown, profile.lore_shown,
                           thorny_user.thorny_id)


async def update_levels(thorny_user: User):
    async with thorny_user.connection_pool.acquire() as conn:
        await conn.execute("""
                           UPDATE thorny.levels
                           SET user_level = $1, xp = $2, required_xp = $3
                           WHERE thorny_user_id = $4
                           """,
                           thorny_user.level.level, thorny_user.level.xp, thorny_user.level.required_xp,
                           thorny_user.thorny_id)


async def update_counters(thorny_user: User):
    counters = thorny_user.counters
    async with thorny_user.connection_pool.acquire() as conn:
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
    async with thorny_user.connection_pool.acquire() as conn:
        await conn.execute("""
                           UPDATE thorny.inventory
                           SET item_id = $1, item_count = $2
                           WHERE inventory_id = $3
                           """,
                           inventory_slot.item_id, inventory_slot.item_count, inventory_slot.inventory_id)


async def insert_inventory_slot(thorny_user: User, inventory_slot: InventorySlot):
    async with thorny_user.connection_pool.acquire() as conn:
        await conn.execute("""
                           INSERT INTO thorny.inventory(thorny_user_id, item_id, item_count)
                           VALUES($1, $2, $3)
                           """,
                           thorny_user.thorny_id, inventory_slot.item_id, inventory_slot.item_count)


async def delete_inventory_slot(thorny_user: User, inventory_slot: InventorySlot):
    async with thorny_user.connection_pool.acquire() as conn:
        await conn.execute("""
                           DELETE FROM thorny.inventory
                           WHERE inventory_id = $1
                           """,
                           inventory_slot.inventory_id)


async def insert_strike(thorny_user: User, strike: Strike):
    async with thorny_user.connection_pool.acquire() as conn:
        await conn.execute("""
                           INSERT INTO thorny.strikes(thorny_user_id, manager_id, reason)
                           VALUES($1, $2, $3)
                           """,
                           strike.strike_id, strike.manager_id, strike.reason)


async def delete_strike(thorny_user: User, strike: Strike):
    async with thorny_user.connection_pool.acquire() as conn:
        await conn.execute("""
                           DELETE FROM thorny.strikes
                           WHERE strike_id = $1
                           """,
                           strike.strike_id)


async def commit(thorny_user: User):
    async with thorny_user.connection_pool.acquire() as conn:
        async with conn.transaction():
            await update_user(thorny_user)
            await update_profile(thorny_user)
            await update_levels(thorny_user)
            await update_counters(thorny_user)

            original_slots = thorny_user.inventory.original_slots
            slots = thorny_user.inventory.slots
            if len(original_slots) > len(slots):
                for slot in original_slots:
                    if slot not in slots:
                        await delete_inventory_slot(thorny_user, slot)
            elif len(slots) > len(original_slots):
                for slot in slots:
                    if slot not in original_slots:
                        await insert_inventory_slot(thorny_user, slot)
            elif len(slots) == len(original_slots):
                for slot in slots:
                    await update_inventory_slot(thorny_user, slot)

            original_strikes = thorny_user.strikes.original_strikes
            strikes = thorny_user.strikes.strikes
            if len(original_strikes) > len(strikes):
                for strike in original_strikes:
                    if strike not in strikes:
                        await delete_strike(thorny_user, strike)
            elif len(strikes) > len(original_strikes):
                for strike in strikes:
                    if strike not in original_strikes:
                        await insert_strike(thorny_user, strike)

            print(f"[{datetime.now().replace(microsecond=0)}] [DATABASE] Committed ThornyUser with "
                  f"Thorny ID", thorny_user.thorny_id)
