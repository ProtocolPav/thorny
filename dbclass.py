import asyncpg
import asyncpg as pg
import asyncio
from datetime import datetime, timedelta
import json
import discord
from thorny_code import errors
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass, field


async def connection():
    config = json.load(open('../thorny_data/config.json', 'r+'))
    pool = await pg.create_pool(database=config['database']['name'],
                                user=config['database']['user'],
                                password=config['database']['password'])
    print("[CONNECT] Successfully connected to Database at", datetime.now())
    return pool


class ThornyFactory:
    @classmethod
    async def build(cls, member: discord.Member):
        conn = await connection()
        user_id = member.id
        guild_id = member.guild.id
        thorny_user = await conn.fetchrow("""SELECT * FROM thorny.user
                                             WHERE user_id = $1 AND guild_id = $2""", user_id, guild_id)
        thorny_id = thorny_user['thorny_user_id']

        user_profile = await conn.fetchrow("""SELECT * FROM thorny.profile
                                              INNER JOIN thorny.levels
                                              ON thorny.levels.thorny_user_id = thorny.profile.thorny_user_id
                                              WHERE thorny.profile.thorny_user_id = $1""", thorny_id)
        user_activity = await conn.fetchrow("""SELECT * FROM thorny.user_activity
                                               WHERE thorny_user_id = $1""", thorny_id)
        user_recent_playtime = await conn.fetchrow("""SELECT playtime FROM thorny.activity
                                                      WHERE thorny_user_id = $1 AND disconnect_time IS NOT NULL
                                                      ORDER BY connect_time DESC""", thorny_id)
        user_strikes = await conn.fetch("""SELECT * from thorny.strikes
                                           WHERE thorny_user_id = $1""", thorny_id)
        user_counters = await conn.fetch("""SELECT * from thorny.counter
                                            WHERE thorny_user_id = $1""", thorny_id)
        master_datalayer = DataLayer(discord_member=member,
                                     connection=conn,
                                     thorny_user=thorny_user,
                                     thorny_user_profile=user_profile,
                                     thorny_user_activity=user_activity,
                                     thorny_user_recent_playtime=user_recent_playtime,
                                     thorny_user_strikes=user_strikes,
                                     thorny_user_counters=user_counters)
        return ThornyUser(master_datalayer)

    @classmethod
    async def create(cls, member: discord.Member):
        conn = await connection()
        user_id = member.id
        guild_id = member.guild.id
        user = await conn.fetchrow("""SELECT * FROM thorny.user
                                      WHERE user_id = $1 AND guild_id = $2""", user_id, guild_id)
        if user is None:
            await conn.execute("""INSERT INTO thorny.user(user_id, guild_id, join_date, balance, username)
                                  VALUES($1, $2, $3, $4, $5)""", user_id, guild_id, datetime.now(), 25, member.name)
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
            print(f"[SERVER] Reactivated account of {user['username']}, Thorny ID {user['thorny_user_id']}")

    @classmethod
    async def deactivate(cls, member: discord.Member):
        conn = await connection()
        thorny_user = await conn.fetchrow("""SELECT * FROM thorny.user
                                             WHERE user_id = $1 AND guild_id = $2""", member.id, member.guild.id)
        thorny_id = thorny_user['thorny_user_id']
        await conn.execute("""UPDATE thorny.user
                              SET active = False WHERE thorny_user_id = $1""", thorny_id)
        print(f"[SERVER] Deactivated account of {thorny_user['username']}, Thorny ID {thorny_id}")


@dataclass
class DataLayer:
    discord_member: discord.Member
    connection: connection()
    thorny_user: pg.Record
    thorny_user_profile: pg.Record
    thorny_user_activity: pg.Record
    thorny_user_recent_playtime: pg.Record
    thorny_user_strikes: pg.Record
    thorny_user_counters: pg.Record


@dataclass
class ThornyUserProfile:
    id: int = field(repr=False)
    conn: connection() = field(repr=False)
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
        self.conn = master_datalayer.connection
        profile = master_datalayer.thorny_user_profile
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
    conn: connection() = field(repr=False)
    total_playtime: timedelta
    current_playtime: timedelta
    previous_playtime: timedelta
    expiring_playtime: timedelta
    recent_session: timedelta = None
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
        self.daily_average = playtime['daily_average']
        self.session_average = playtime['session_average']
        if master_datalayer.thorny_user_recent_playtime is not None:
            self.recent_session = master_datalayer.thorny_user_recent_playtime['playtime']

    async def connect(self):
        recent_connection = await self.conn.fetchrow("""SELECT * FROM thorny.activity
                                                        WHERE thorny_user_id = $1
                                                        ORDER BY connect_time DESC""", self.id)
        if recent_connection is None or recent_connection['disconnect_time'] is not None:
            await self.conn.execute("INSERT INTO thorny.activity(thorny_user_id, connect_time) "
                                    "VALUES($1, $2)", self.id, datetime.now().replace(microsecond=0))
            already_connected = False
        elif datetime.now() - recent_connection['connect_time'] > timedelta(hours=12):
            playtime = timedelta(hours=1, minutes=5)
            await self.conn.execute("UPDATE thorny.activity SET disconnect_time = $1, playtime = $2 "
                                    "WHERE thorny_user_id = $3 and connect_time = $4",
                                    datetime.now().replace(microsecond=0), playtime,
                                    self.id, recent_connection['connect_time'])

            await self.conn.execute("INSERT INTO thorny.activity(thorny_user_id, connect_time) "
                                    "VALUES($1, $2)", self.id, datetime.now().replace(microsecond=0))
            already_connected = False
        else:
            already_connected = True
        return already_connected

    async def disconnect(self, journal_entry):
        recent_connection = await self.conn.fetchrow("""SELECT * FROM thorny.activity
                                                        WHERE thorny_user_id = $1
                                                        ORDER BY connect_time DESC""", self.id)
        if recent_connection is None or recent_connection['disconnect_time'] is not None:
            not_connected = True
            overtime = False
            playtime = None
        else:
            not_connected = False
            playtime = datetime.now().replace(microsecond=0) - recent_connection['connect_time']
            overtime = False
            if playtime > timedelta(hours=12):
                overtime = True
                playtime = timedelta(hours=1, minutes=5)
            await self.conn.execute("""UPDATE thorny.activity SET disconnect_time = $1, playtime = $2, description = $5
                                       WHERE thorny_user_id = $3 and connect_time = $4""",
                                    datetime.now().replace(microsecond=0), playtime,
                                    self.id, recent_connection['connect_time'], journal_entry)
        return not_connected, overtime, playtime

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
        if slot is not None:
            self.inventory_id = slot['inventory_id']
            self.item_id = slot['item_id']
            self.item_display_name = slot['display_name']
            self.item_count = slot['item_count']


@dataclass
class ThornyUserStrikes:
    id: int = field(repr=False)
    conn: connection() = field(repr=False)
    strike_list: list

    def __init__(self, master_datalayer):
        self.id = master_datalayer.thorny_user['thorny_user_id']
        self.conn = master_datalayer.connection
        self.strike_list = []
        for strike in master_datalayer.thorny_user_strikes:
            self.strike_list.append({
                "id": strike['strike_id'],
                "manager_id": strike['manager_id'],
                "reason": strike['reason']
            })


@dataclass
class ThornyUserCounters:
    id: int = field(repr=False)
    conn: connection() = field(repr=False)
    tickets: int = None
    tickets_last_purchase: datetime = None
    levels_last_message: datetime = None

    def __init__(self, master_datalayer):
        self.id = master_datalayer.thorny_user['thorny_user_id']
        self.conn = master_datalayer.connection
        counters = master_datalayer.thorny_user_counters
        for counter in counters:
            if counter['counter_name'] == 'ticket_count':
                self.tickets = counter['count']
            elif counter['counter_name'] == 'ticket_last_purchase':
                self.tickets_last_purchase = counter['datetime']
            elif counter['counter_name'] == 'level_last_message':
                self.levels_last_message = counter['datetime']


@dataclass
class ThornyUser:
    conn: connection() = field(repr=False)
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
        self.conn = master_datalayer.connection
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
        await self.conn.execute(f"""UPDATE thorny.user 
                                    SET {attribute} = $1 
                                    WHERE thorny_user_id = $2""", value, self.id)
