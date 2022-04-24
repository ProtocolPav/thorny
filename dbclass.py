import asyncpg
import asyncpg as pg
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
import discord
import errors
from dataclasses import dataclass, field
from connection_pool import pool


@dataclass
class ThornyUserProfile:
    id: int = field(repr=False)
    pool: pg.Pool = field(repr=False)
    level: int
    xp: int
    required_xp: int
    last_message: datetime = None
    slogan: str = None
    gamertag: str = None
    town: str = None
    role: str = None
    wiki: str = None
    aboutme: str = None
    lore: str = None
    information_shown: bool = True
    aboutme_shown: bool = True
    activity_shown: bool = True
    lore_shown: bool = True
    wiki_shown: bool = True

    def __init__(self, master_datalayer):
        self.pool = master_datalayer.connection_pool
        profile = master_datalayer.profile
        self.id = profile['thorny_user_id']
        self.slogan = profile['slogan']
        self.gamertag = profile['gamertag']
        self.town = profile['town']
        self.role = profile['role']
        self.wiki = profile['wiki']
        self.aboutme = profile['aboutme']
        self.lore = profile['lore']
        self.information_shown = profile['information_shown']
        self.activity_shown = profile['activity_shown']
        self.lore_shown = profile['lore_shown']
        self.wiki_shown = profile['wiki_shown']

        self.level = profile['user_level']
        self.xp = profile['xp']
        self.required_xp = profile['required_xp']
        self.last_message = profile['last_message']

    async def update(self, section, value):
        self.__setattr__(section, value)
        try:
            await self.conn.execute(f"""UPDATE thorny.profile
                                        SET {section} = $1
                                        WHERE thorny_user_id = $2""", value, self.id)
        except asyncpg.StringDataRightTruncationError:
            return errors.Profile.length_error

    async def toggle(self, category):
        self.__setattr__(category, not category)
        await self.conn.execute(f"""UPDATE thorny.profile
                                    SET {category} = NOT {category}
                                    WHERE thorny_user_id = $1""", self.id)


@dataclass
class ThornyUserPlaytime:
    id: int = field(repr=False)
    pool: pg.Pool = field(repr=False)
    total_playtime: timedelta = None
    current_playtime: timedelta = None
    previous_playtime: timedelta = None
    expiring_playtime: timedelta = None
    recent_session: timedelta = None
    daily_average: timedelta = None
    session_average: timedelta = None

    def __init__(self, master_datalayer):
        self.pool = master_datalayer.connection_pool
        playtime = master_datalayer.playtime
        stats = master_datalayer.playtime_stats
        self.id = playtime['thorny_user_id']
        self.session_average = playtime['session_average']
        if stats is not None:
            self.total_playtime = stats['total_playtime']
            self.current_playtime = stats['current_playtime']
            self.previous_playtime = stats['previous_playtime']
            self.expiring_playtime = stats['expiring_playtime']
        if master_datalayer.daily_average is not None:
            self.daily_average = master_datalayer.daily_average['averages']
        if master_datalayer.recent_playtime is not None:
            self.recent_session = master_datalayer.recent_playtime['playtime']

    # Adjust must be changed to be in dbevent.py

    async def adjust(self, hour, minute):
        recent_connection = await self.conn.fetchrow("""SELECT * FROM thorny.activity
                                                        WHERE thorny_user_id = $1
                                                        ORDER BY connect_time DESC""", self.id)
        if recent_connection is None or recent_connection['disconnect_time'] is None:
            already_connected = True
        else:
            already_connected = False
            playtime = recent_connection['playtime'] - timedelta(hours=hour or 0, minutes=minute or 0)
            desc = f"Adjusted by {hour or 0}h{minute or 0}m | {recent_connection['description']}"
            await self.conn.execute("""UPDATE thorny.activity SET playtime = $1, description = $2
                                       WHERE thorny_user_id = $3 and connect_time = $4""",
                                    playtime, desc, self.id, recent_connection['connect_time'])
        return already_connected


@dataclass
class ThornyUserSlot:
    id: int = field(repr=False)
    pool: pg.Pool = field(repr=False)
    inventory_id: int
    item_id: str
    item_display_name: str
    item_count: int
    item_max_count: int
    item_cost: int
    redeemable: bool

    def __init__(self, thorny_id, pool, slot):
        self.id = thorny_id
        self.pool = pool
        self.inventory_id = slot['inventory_id']
        self.item_id = slot['item_id']
        self.item_count = slot['item_count']
        self.item_display_name = slot['display_name']
        self.item_max_count = slot['max_item_count']
        self.item_cost = slot['item_cost']
        self.redeemable = slot['redeemable']


@dataclass
class ThornyUserInventory:
    id: int = field(repr=False)
    pool: pg.Pool = field(repr=False)
    original_slots: list[ThornyUserSlot] = field(repr=False)
    all_item_metadata: list = field(repr=False)
    slots: list[ThornyUserSlot]

    def __init__(self, master_datalayer):
        self.id = master_datalayer.thorny_user['thorny_user_id']
        self.pool = master_datalayer.connection_pool
        self.slots = []
        self.all_item_metadata = []
        for slot in master_datalayer.inventory:
            self.slots.append(ThornyUserSlot(self.id, self.pool, slot))
        for item in master_datalayer.item_data:
            self.all_item_metadata.append(item)
        self.original_slots = self.slots

    async def fetch_slot(self, item_id):
        slot = await self.conn.fetchrow("""SELECT inventory_id, item_id, item_count
                                           FROM thorny.inventory
                                           WHERE thorny_user_id = $1 AND item_id = $2""",
                                        self.id, item_id)
        item_data = await self.conn.fetchrow("""SELECT display_name, max_item_count, item_cost
                                                FROM thorny.item_type
                                                WHERE friendly_id = $1""", item_id)
        self.item_display_name = item_data['display_name']
        self.item_max_count = item_data['max_item_count']
        self.item_cost = item_data['item_cost']

        if slot is not None:
            self.inventory_id = slot['inventory_id']
            self.item_id = slot['item_id']
            self.item_count = slot['item_count']

    async def update_count(self, count):
        self.__setattr__("item_count", count)
        await self.conn.execute(f"""UPDATE thorny.inventory 
                                    SET item_count = $1 
                                    WHERE inventory_id = $2""", count, self.inventory_id)

    def append(self, item_id, count):
        for item_data in self.all_item_metadata:
            if item_data["friendly_id"] == item_id and count <= item_data["max_item_count"]:
                item = {
                    "inventory_id": 0,
                    "item_id": item_id,
                    "item_count": count,
                    "display_name": item_data["display_name"],
                    "max_item_count": item_data["max_item_count"],
                    "item_cost": item_data["item_cost"],
                    "redeemable": item_data["redeemable"]
                }
                self.slots.append(ThornyUserSlot(None, None, item))
                return False
            else:
                return True

    async def delete(self):
        await self.conn.execute("""DELETE FROM thorny.inventory WHERE inventory_id = $1""", self.inventory_id)


@dataclass
class ThornyUserStrike:
    id: int = field(repr=False)
    pool: pg.Pool = field(repr=False)
    strike_id: int
    manager_id: int
    reason: str

    def __init__(self, thorny_id, pool, strike):
        self.id = thorny_id
        self.pool = pool
        self.strike_id = strike['strike_id']
        self.manager_id = strike['manager_id']
        self.reason = strike['reason']


@dataclass
class ThornyUserStrikes:
    id: int = field(repr=False)
    pool: pg.Pool = field(repr=False)
    original_strikes: list[ThornyUserStrike]
    strikes: list[ThornyUserStrike]

    def __init__(self, master_datalayer):
        self.id = master_datalayer.thorny_user['thorny_user_id']
        self.pool = master_datalayer.connection_pool
        self.strikes = []
        for strike in master_datalayer.strikes:
            self.strikes.append(ThornyUserStrike(self.id, self.pool, strike))
        self.original_strikes = self.strikes

    async def insert(self, manager: discord.Member, reason: str):
        await self.conn.execute("""
                                INSERT INTO thorny.strikes(thorny_user_id, manager_id, reason)
                                VALUES($1, $2, $3)
                                """,
                                self.id, manager.id, reason)
        strike_id = await self.conn.fetchrow('SELECT strike_id '
                                             'FROM thorny.strikes '
                                             'ORDER BY strike_id DESC')


@dataclass
class ThornyUserCounters:
    id: int = field(repr=False)
    pool: pg.Pool = field(repr=False)
    ticket_count: int
    ticket_last_purchase: datetime
    level_last_message: datetime

    def __init__(self, master_datalayer):
        self.id = master_datalayer.thorny_user['thorny_user_id']
        self.pool = master_datalayer.connection_pool
        counters = master_datalayer.counters
        for counter in counters:
            if counter['counter_name'] == 'ticket_count':
                self.ticket_count = counter['count']
            elif counter['counter_name'] == 'ticket_last_purchase':
                self.ticket_last_purchase = counter['datetime']
            elif counter['counter_name'] == 'level_last_message':
                self.level_last_message = counter['datetime']

    async def update(self, counter: str, value):
        self.__setattr__(counter, value)
        if type(value) == int:
            await self.conn.execute(f"""UPDATE thorny.counter SET count=$1 
                                        WHERE thorny_user_id = $2 AND counter_name = $3""", value, self.id, counter)
        else:
            await self.conn.execute(f"""UPDATE thorny.counter SET datetime=$1 
                                        WHERE thorny_user_id = $2 AND counter_name = $3""", value, self.id, counter)

    async def commit(self):
        await self.conn.execute("""
                                UPDATE thorny.counter
                                SET count = $1 
                                WHERE thorny_user_id = $2 AND counter_name = $3
                                """,
                                self.ticket_count, self.id, "ticket_count")
        await self.conn.execute("""
                                UPDATE thorny.counter
                                SET ticket_last_purchase = $1 
                                WHERE thorny_user_id = $2 AND counter_name = $3
                                """,
                                self.ticket_last_purchase, self.id, "ticket_last_purchase")


@dataclass
class ThornyUser:
    pool: pg.Pool = field(repr=False)
    member_object: discord.Member = field(repr=False)
    id: int
    discord_id: int
    guild_id: int
    username: str
    balance: int
    kingdom: str
    join_date: datetime
    birthday: datetime
    profile: ThornyUserProfile
    playtime: ThornyUserPlaytime
    inventory: ThornyUserInventory
    strikes: ThornyUserStrikes
    counters: ThornyUserCounters

    def __init__(self, master_datalayer):
        self.pool = master_datalayer.connection_pool
        self.member_object = master_datalayer.discord_member
        user = master_datalayer.thorny_user
        self.id = user['thorny_user_id']
        self.username = self.member_object.name
        self.guild_id = user['guild_id']
        self.discord_id = user['user_id']
        self.balance = user['balance']
        self.kingdom = user['kingdom']
        self.join_date = user['join_date']
        self.birthday = user['birthday']
        self.profile = ThornyUserProfile(master_datalayer)
        self.playtime = ThornyUserPlaytime(master_datalayer)
        self.inventory = ThornyUserInventory(master_datalayer)
        self.strikes = ThornyUserStrikes(master_datalayer)
        self.counters = ThornyUserCounters(master_datalayer)

    async def update(self, attribute, value):
        self.__setattr__(attribute, value)
        async with self.pool.acquire() as conn:
            await conn.execute(f"""UPDATE thorny.user 
                                        SET {attribute} = $1 
                                        WHERE thorny_user_id = $2""", value, self.id)

    def calculate_ticket_reward(self, prize_list, prizes):
        nugs_reward = 0
        for item in prize_list:
            nugs_reward += item[1]
        if prize_list[0] != prize_list[1] != prize_list[2] != prize_list[3] and prizes[5] not in prize_list:
            nugs_reward = nugs_reward * 2
        return nugs_reward
