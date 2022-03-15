import asyncpg
import asyncpg as pg
import asyncio
from datetime import datetime, timedelta
import json
import discord
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass, field


async def connection():
    pool = await pg.create_pool(database='postgres', user='postgres', password='p@v3LPlay%MC')
    return pool


class ThornyFactory:
    @classmethod
    async def build(cls, user_id, guild_id):
        conn = await connection()
        thorny_user = await conn.fetchrow("""SELECT * FROM thorny.user
                                                       WHERE user_id = $1 AND guild_id = $2""", user_id, guild_id)
        thorny_id = thorny_user['thorny_user_id']

        user_profile = await conn.fetchrow("""SELECT * FROM thorny.profile
                                              WHERE thorny_user_id = $1""", thorny_id)
        user_activity = await conn.fetchrow("""SELECT * FROM thorny.user_activity
                                               WHERE thorny_user_id = $1""", thorny_id)
        user_recent_playtime = await conn.fetchrow("""SELECT playtime FROM thorny.activity
                                                      WHERE thorny_user_id = $1 AND disconnect_time IS NOT NULL
                                                      ORDER BY connect_time DESC""", thorny_id)
        master_datalayer = DataLayer(connection=conn,
                                     thorny_user=thorny_user,
                                     thorny_user_profile=user_profile,
                                     thorny_user_activity=user_activity,
                                     thorny_user_recent_playtime=user_recent_playtime)
        return ThornyUser(master_datalayer)


@dataclass
class DataLayer:
    connection: connection()
    thorny_user: pg.Record
    thorny_user_profile: pg.Record
    thorny_user_activity: pg.Record
    thorny_user_recent_playtime: pg.Record


@dataclass
class ThornyUserProfile:
    id: int = field(repr=False)
    conn: connection() = field(repr=False)
    slogan: str = None
    gamertag: str = None
    town: str = None
    role: str = None
    wiki: str = None
    biography: str = None
    lore: str = None
    information_shown: bool = True
    aboutme_shown: bool = True
    activity_shown: bool = True
    lore_shown: bool = True
    wiki_shown: bool = True

    def __init__(self, master_datalayer):
        self.conn = master_datalayer.connection
        profile = master_datalayer.thorny_user_profile
        self.id = profile['thorny_user_id']
        self.slogan = profile['slogan']
        self.gamertag = profile['gamertag']
        self.town = profile['town']
        self.role = profile['role']
        self.wiki = profile['wiki']
        self.biography = profile['aboutme']
        self.lore = profile['lore']
        self.information_shown = profile['information_shown']
        self.activity_shown = profile['activity_shown']
        self.lore_shown = profile['lore_shown']
        self.wiki_shown = profile['wiki_shown']


@dataclass
class ThornyUserPlaytime:
    id: int = field(repr=False)
    conn: connection() = field(repr=False)
    total_playtime: timedelta
    current_playtime: timedelta
    previous_playtime: timedelta
    expiring_playtime: timedelta
    recent_session: timedelta
    daily_average: timedelta = None
    session_average: timedelta = None

    def __init__(self, master_datalayer):
        self.conn = master_datalayer.connection
        playtime = master_datalayer.thorny_user_activity
        self.id = playtime['thorny_user_id']
        self.total_playtime = playtime['total_playtime']
        self.current_playtime = playtime['current_month']
        self.previous_playtime = playtime['one_month_ago']
        self.expiring_playtime = playtime['two_months_ago']
        self.recent_session = master_datalayer.thorny_user_recent_playtime['playtime']
        self.daily_average = playtime['daily_average']
        self.session_average = playtime['session_average']


@dataclass
class ThornyUserInventory:
    """
    Class which stores a single inventory slot at a time
    """
    id: int = field(repr=False)
    conn: connection() = field(repr=False)
    inventory_id: int = None
    item_id: str = None
    item_display_name: str = None
    item_count: int = None

    def __init__(self, master_datalayer):
        self.id = master_datalayer.thorny_user['thorny_user_id']
        self.conn = master_datalayer.connection

    async def get_all_slots(self):
        return await self.conn.fetch("""SELECT inventory_id, item_id, item_count, display_name FROM thorny.inventory
                                        INNER JOIN thorny.item_type ON friendly_id=item_id
                                        WHERE thorny_user_id = $1""", self.id)

    async def fetch_slot(self, item_id):
        slot = await self.conn.fetchrow("""SELECT inventory_id, item_id, item_count, display_name FROM thorny.inventory
                                           INNER JOIN thorny.item_type ON friendly_id=item_id
                                           WHERE thorny_user_id = $1 AND item_id = $2""", self.id, item_id)
        self.inventory_id = slot['inventory_id']
        self.item_id = slot['item_id']



@dataclass
class ThornyUser:
    conn: connection() = field(repr=False)
    id: int
    user_id: int
    guild_id: int
    username: str
    balance: int
    kingdom: str
    profile: ThornyUserProfile
    playtime: ThornyUserPlaytime
    inventory: ThornyUserInventory

    def __init__(self, master_datalayer):
        self.conn = master_datalayer.connection
        user = master_datalayer.thorny_user
        self.id = user['thorny_user_id']
        self.username = user['username']
        self.guild_id = user['guild_id']
        self.user_id = user['user_id']
        self.balance = user['balance']
        self.kingdom = user['kingdom']
        self.profile = ThornyUserProfile(master_datalayer)
        self.playtime = ThornyUserPlaytime(master_datalayer)
        self.inventory = ThornyUserInventory(master_datalayer)


