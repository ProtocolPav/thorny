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

# conn = asyncio.get_event_loop().run_until_complete(connection())


async def fetch_thorny_user(user_id, guild_id):
    conn = await connection()
    thorny_user_datalayer = await conn.fetchrow("""SELECT * FROM thorny.user
                                             WHERE user_id = $1 AND guild_id = $2""", user_id, guild_id)
    return ThornyUser(thorny_user_datalayer)


@dataclass
class ThornyUserProfile:
    id: int = field(repr=False, default=None)
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

    def __init__(self, thorny_id):
        temp = asyncio.new_event_loop().run_until_complete(conn.fetchrow("""SELECT * FROM thorny.profile
                                      WHERE thorny_user_id = $1""", thorny_id))
        self.id = temp['thorny_user_id']
        self.slogan = temp['slogan']
        self.gamertag = temp['gamertag']
        self.town = temp['town']
        self.role = temp['role']
        self.wiki = temp['wiki']
        self.biography = temp['aboutme']
        self.lore = temp['lore']
        self.information_shown = temp['information_shown']
        self.activity_shown = temp['activity_shown']
        self.lore_shown = temp['lore_shown']
        self.wiki_shown = temp['wiki_shown']


@dataclass
class ThornyUser:
    id: int
    user_id: int
    guild_id: int
    username: str
    balance: int
    kingdom: str
    # profile: ThornyUserProfile
    # activity: ThornyUserActivity = None
    # inventory: ThornyUserInventory = None

    def __init__(self, datalayer):
        self.id = datalayer['thorny_user_id']
        self.username = datalayer['username']
        self.guild_id = datalayer['guild_id']
        self.user_id = datalayer['user_id']
        self.balance = datalayer['balance']
        self.kingdom = datalayer['kingdom']


