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

    def update(self, attribute, value=None, toggle=False):
        if toggle:
            toggler = self.__getattribute__(attribute)
            self.__setattr__(attribute, not toggler)
        else:
            self.__setattr__(attribute, value)


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

    def __init__(self, thorny_id, pool_object, slot):
        self.id = thorny_id
        self.pool = pool_object
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
        self.original_slots = []
        self.all_item_metadata = []
        for slot in master_datalayer.inventory:
            self.slots.append(ThornyUserSlot(self.id, self.pool, slot))
            self.original_slots.append(ThornyUserSlot(self.id, self.pool, slot))
        for item in master_datalayer.item_data:
            self.all_item_metadata.append(item)

    def append(self, item_id, count):
        error = False
        added = False
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
                self.slots.append(ThornyUserSlot(self.id, self.pool, item))
                error = False
                added = True
                return error, added
            else:
                error = True
                added = False
        return error, added

    def fetch(self, item_id):
        for item in self.slots:
            if item.item_id == item_id:
                return item
            else:
                return None


@dataclass
class ThornyUserStrike:
    id: int = field(repr=False)
    pool: pg.Pool = field(repr=False)
    strike_id: int
    manager_id: int
    reason: str

    def __init__(self, thorny_id, pool_object, strike):
        self.id = thorny_id
        self.pool = pool_object
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

    async def append(self, manager_id, reason):
        strike = {
            "strike_id": 0,
            "manager_id": manager_id,
            "reason": reason
        }
        self.strikes.append(ThornyUserStrike(self.id, self.pool, strike))


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
