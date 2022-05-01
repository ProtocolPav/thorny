import asyncpg
import asyncpg as pg
import asyncio
from datetime import datetime, timedelta
import json
import discord
from dateutil.relativedelta import relativedelta


async def connection():
    config = json.load(open('../thorny_data/config.json', 'r+'))
    pool = await pg.create_pool(database=config['database']['name'],
                                user=config['database']['user'],
                                password=config['database']['password'])
    return pool

conn = asyncio.get_event_loop().run_until_complete(connection())


async def create_thorny_database(ctx):
    await conn.execute("DROP SCHEMA thorny CASCADE")
    await conn.execute("CREATE SCHEMA thorny")
    await conn.execute("CREATE TABLE thorny.user ("
                       "thorny_user_id bigserial,"
                       "user_id int8 NOT NULL,"
                       "guild_id int8 NOT NULL,"
                       "username varchar,"
                       "join_date date,"
                       "birthday date,"
                       "kingdom varchar,"
                       "balance int4,"
                       "playing bool DEFAULT true,"
                       "server_role varchar,"
                       "PRIMARY KEY(thorny_user_id))")
    await conn.execute("CREATE TABLE thorny.activity("
                       "thorny_user_id int8 NOT NULL,"
                       "user_id int8,"
                       "guild_id int8,"
                       "playtime interval,"
                       "connect_time timestamp,"
                       "disconnect_time timestamp,"
                       "description varchar(275),"
                       "FOREIGN KEY(thorny_user_id) REFERENCES thorny.user(thorny_user_id))")
    await conn.execute("CREATE TABLE thorny.counter("
                       "thorny_user_id int8 NOT NULL,"
                       "user_id int8,"
                       "guild_id int8,"
                       "counter_name varchar,"
                       "count int,"
                       "datetime timestamp,"
                       "FOREIGN KEY(thorny_user_id) REFERENCES thorny.user(thorny_user_id))")
    await conn.execute('CREATE TABLE thorny.inventory('
                       'inventory_id serial,'
                       "thorny_user_id int8 NOT NULL,"
                       "user_id int8,"
                       "guild_id int8,"
                       'item_id varchar,'
                       'item_count int,'
                       'PRIMARY KEY(inventory_id),'
                       'FOREIGN KEY(thorny_user_id) REFERENCES thorny.user(thorny_user_id))')
    await conn.execute("CREATE TABLE thorny.item_type("
                       "unique_id serial,"
                       "friendly_id varchar,"
                       "display_name varchar,"
                       "max_item_count int4 DEFAULT 8,"
                       "item_cost int4 DEFAULT 0,"
                       "PRIMARY KEY(unique_id))")
    await conn.execute('CREATE TABLE thorny.kingdoms('
                       'kingdom_id serial,'
                       'kingdom varchar,'
                       'treasury int4,'
                       'emoji varchar,'
                       'ruler_name varchar,'
                       'ruler_id int8,'
                       'capital varchar,'
                       'alliances varchar,'
                       'town_count int,'
                       'slogan varchar,'
                       'border_type varchar,'
                       'gov_type varchar,'
                       'creation_date timestamp,'
                       'description varchar(450),'
                       'PRIMARY KEY(kingdom_id))')
    await conn.execute("CREATE TABLE thorny.levels("
                       "thorny_user_id int8 NOT NULL,"
                       "user_id int8,"
                       "guild_id int8,"
                       "user_level int DEFAULT 0,"
                       "xp int DEFAULT 0,"
                       "required_xp int DEFAULT 100,"
                       "last_message timestamp,"
                       "FOREIGN KEY(thorny_user_id) REFERENCES thorny.user(thorny_user_id))")
    await conn.execute("CREATE TABLE thorny.profile("
                       "thorny_user_id int8 NOT NULL,"
                       "user_id int8,"
                       "guild_id int8,"
                       "slogan varchar(35),"
                       "gamertag varchar,"
                       "town varchar(50),"
                       "role varchar(50),"
                       "wiki varchar,"
                       "aboutme varchar(300),"
                       "lore varchar(300),"
                       "information_shown bool DEFAULT true,"
                       "aboutme_shown bool DEFAULT true,"
                       "activity_shown bool DEFAULT true,"
                       "wiki_shown bool DEFAULT true,"
                       "lore_shown bool DEFAULT true,"
                       "PRIMARY KEY(thorny_user_id),"
                       "FOREIGN KEY(thorny_user_id) REFERENCES thorny.user(thorny_user_id))")
    await conn.execute("CREATE TABLE thorny.strike_list("
                       "strike_id int,"
                       "thorny_user_id int8 NOT NULL,"
                       "reason varchar,"
                       "manager_id int8,"
                       "PRIMARY KEY(strike_id),"
                       "FOREIGN KEY(thorny_user_id) REFERENCES thorny.user(thorny_user_id))")
    await conn.execute("CREATE TABLE thorny.user_activity("
                       "thorny_user_id int8 NOT NULL,"
                       "user_id int8,"
                       "guild_id int8,"
                       "total_playtime interval,"
                       "current_month interval,"
                       "one_month_ago interval,"
                       "two_months_ago interval,"
                       "daily_average interval,"
                       "session_average interval,"
                       "weekly_average interval,"
                       "PRIMARY KEY(thorny_user_id),"
                       "FOREIGN KEY(thorny_user_id) REFERENCES thorny.user(thorny_user_id))")
    await ctx.send(f"Created the Database!")


async def populate_tables(ctx):
    await conn.execute("INSERT INTO thorny.user(thorny_user_id, username, user_id, guild_id)"
                       "VALUES($1, $2, $3, $4)", 0, 'SERVER', 0, 0)
    await conn.execute("INSERT INTO thorny.item_type "
                       "VALUES($1, $2, $3, $4, $5)", 1, 'role', 'Custom Role Voucher', 8, 0)
    await conn.execute("INSERT INTO thorny.item_type "
                       "VALUES($1, $2, $3, $4, $5)", 2, 'ticket', 'Scratch Ticket', 8, 14)
    await conn.execute("INSERT INTO thorny.item_type "
                       "VALUES($1, $2, $3, $4, $5)", 3, 'present', 'Christmas Present', 3, 0)
    await conn.execute("INSERT INTO thorny.item_type "
                       "VALUES($1, $2, $3, $4, $5)", 4, 'gift', 'Birthday Gift', 1, 0)
    await ctx.send("Item_type table populated")
    await conn.execute("INSERT INTO thorny.counter(user_id, counter_name, count, thorny_user_id, guild_id) "
                       "VALUES($1, $2, $3, $4, $5)", 0, 'ticket_count', 626, 0, 0)
    await ctx.send("Ticket Counter added to counter table\n Populating Kingdoms table")
    config = json.load(open('../thorny_data/config.json', 'r+'))
    treasury = json.load(open('../thorny_data/kingdoms.json', 'r+'))
    for kingdom in treasury:
        await conn.execute("INSERT INTO thorny.kingdoms(kingdom, treasury, ruler_name, capital, alliances, town_count,"
                           "slogan, border_type, gov_type, description) "
                           "VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)", kingdom.capitalize(), treasury[kingdom],
                           config['kingdoms'][kingdom]['ruler'], config['kingdoms'][kingdom]['capital'],
                           config['kingdoms'][kingdom]['alliances'], int(config['kingdoms'][kingdom]['towns']),
                           config['kingdoms'][kingdom]['slogan'], config['kingdoms'][kingdom]['borders'],
                           config['kingdoms'][kingdom]['government'], config['kingdoms'][kingdom]['description'])
    await ctx.send("Kingdoms table populated")


async def condition_select(table, column, condition, condition_req):
    return await conn.fetch(f"SELECT {column} FROM thorny.{table} WHERE {condition}=$1", condition_req)


async def simple_select(table, column):
    return await conn.fetch(f"SELECT {column} FROM thorny.{table}")


async def simple_update(table, column, new_val, condition, condition_requirement):
    await conn.execute(f"UPDATE thorny.{table} "
                       f"SET {column}=$1"
                       f"WHERE {condition}=$2", new_val, condition_requirement)


async def create_user(member):
    if await conn.fetchrow('SELECT * FROM thorny.user WHERE user_id = $1 AND guild_id = $2',
                           member.id, member.guild.id) is None:
        await conn.execute('INSERT INTO thorny.user(user_id, guild_id, username, join_date, balance) '
                           'VALUES($1, $2, $3, $4, $5)', member.id, member.guild.id, member.discriminator,
                           datetime.now(), 25)
        thorny_id = await conn.fetchrow('SELECT thorny_user_id FROM thorny.user WHERE user_id=$1 AND guild_id=$2',
                                        member.id, member.guild.id)
        await conn.execute("INSERT INTO thorny.user_activity(thorny_user_id, user_id, guild_id)"
                           "VALUES($1, $2, $3)", thorny_id[0], member.id, member.guild.id)
        await conn.execute("INSERT INTO thorny.profile(thorny_user_id, user_id, guild_id)"
                           "VALUES($1, $2, $3)", thorny_id[0], member.id, member.guild.id)
        await conn.execute("INSERT INTO thorny.levels(thorny_user_id, user_id, guild_id)"
                           "VALUES($1, $2, $3)", thorny_id[0], member.id, member.guild.id)
        print(f"{member} has been registered")


def select_all_guilds(client):
    returned_guilds = []
    for guild in client.guilds:
        returned_guilds.append(guild.id)
    return returned_guilds


async def insert_counters(thorny_id):
    await conn.execute("""INSERT INTO thorny.counter(thorny_user_id, counter_name, count)
                                              VALUES($1, $2, $3)""", thorny_id, 'ticket_count', 0)
    await conn.execute("""INSERT INTO thorny.counter(thorny_user_id, counter_name, datetime)
                                              VALUES($1, $2, $3)""", thorny_id, 'ticket_last_purchase',
                       datetime.now())
    await conn.execute("""INSERT INTO thorny.counter(thorny_user_id, counter_name, datetime)
                                              VALUES($1, $2, $3)""", thorny_id, 'level_last_message', datetime.now())


class Inventory:
    """
    Needs updating, make all of them use the member object instead of user_id
    """

    @staticmethod
    async def select(item_id, user_id):
        return await conn.fetchrow(f"SELECT * FROM thorny.inventory WHERE user_id=$1 AND item_id=$2", user_id, item_id)

    @staticmethod
    async def delete(item_id, user_id):
        await conn.execute("DELETE FROM thorny.inventory WHERE user_id=$1 AND item_id =$2", user_id, item_id)

    @staticmethod
    async def insert(item_id, item_count, member):
        thorny_id = await conn.fetchrow('SELECT thorny_user_id FROM thorny.user WHERE user_id=$1 AND guild_id=$2',
                                        member.id, member.guild.id)
        await conn.execute(f"INSERT INTO thorny.inventory(user_id, item_id, item_count, thorny_user_id)"
                           f"VALUES($1, $2, $3, $4)", member.id, item_id, item_count, thorny_id[0])

    @staticmethod
    async def update(item_id, item_count, user_id):
        await conn.execute(f"UPDATE thorny.inventory SET item_count=$1 WHERE user_id=$2 AND item_id=$3",
                           item_count, user_id, item_id)

    @staticmethod
    async def get_item_type(item):
        try:
            int(item)
        except ValueError:
            return await conn.fetchrow(f"SELECT * FROM thorny.item_type WHERE friendly_id=$1",
                                       item)
        else:
            return await conn.fetchrow(f"SELECT * FROM thorny.item_type WHERE unique_id=$1",
                                       int(item))

    @staticmethod
    async def update_item_price(item, price):
        try:
            int(item)
        except ValueError:
            await conn.execute(f"UPDATE thorny.item_type SET item_cost = $2 WHERE friendly_id=$1",
                               item, int(price))
            return True
        else:
            await conn.execute(f"UPDATE thorny.item_type SET item_cost = $2 WHERE unique_id=$1",
                               int(item), int(price))
            return True


class Activity:
    @staticmethod
    async def select_recent_connect(user_id):
        return await conn.fetchrow("SELECT * FROM thorny.activity WHERE user_id = $1 ORDER BY connect_time DESC",
                                   user_id)

    @staticmethod
    async def select_online():
        return await conn.fetch("SELECT * FROM thorny.activity "
                                "JOIN thorny.user ON thorny.user.thorny_user_id = thorny.activity.thorny_user_id "
                                "WHERE disconnect_time is NULL AND connect_time > $1 "
                                "ORDER BY connect_time DESC", datetime.now().replace(day=1))

    @staticmethod
    async def insert_connect(ctx):
        thorny_id = await conn.fetchrow('SELECT thorny_user_id FROM thorny.user WHERE user_id=$1 AND guild_id=$2',
                                        ctx.author.id, ctx.author.guild.id)
        await conn.execute("INSERT INTO thorny.activity(thorny_user_id, user_id, connect_time, guild_id) "
                           "VALUES($1, $2, $3, $4)", thorny_id[0], ctx.author.id, datetime.now().replace(microsecond=0),
                           ctx.author.guild.id)

    @staticmethod
    async def update_disconnect(user_id, connect_time, playtime=None):
        await conn.execute("UPDATE thorny.activity SET disconnect_time = $1, playtime = $2 "
                           "WHERE user_id = $3 and connect_time = $4",
                           datetime.now(), playtime, user_id, connect_time)

    @staticmethod
    async def update_adjust(user_id, connect_time, playtime):
        await conn.execute("UPDATE thorny.activity SET playtime = $1 "
                           "WHERE user_id = $2 and connect_time = $3",
                           playtime, user_id, connect_time)

    @staticmethod
    async def update_user_activity(ctx):
        thorny_id = await conn.fetchrow('SELECT thorny_user_id FROM thorny.user WHERE user_id=$1 AND guild_id=$2',
                                        ctx.author.id, ctx.author.guild.id)
        total_hours = await conn.fetchrow("SELECT SUM(playtime) FROM thorny.activity WHERE user_id = $1",
                                          ctx.author.id)
        current_month_hours = await conn.fetchrow("SELECT SUM(playtime) FROM thorny.activity WHERE user_id = $1 "
                                                  "AND connect_time >= $2",
                                                  ctx.author.id,
                                                  datetime.now().replace(day=1, hour=0, minute=0, second=0,
                                                                         microsecond=0))
        await conn.execute('UPDATE thorny.user_activity '
                           'SET total_playtime = $1, current_month = $2 '
                           'WHERE user_id = $3', total_hours['sum'], current_month_hours['sum'],
                           ctx.author.id)

    @staticmethod
    async def update_user_months():
        await conn.execute('UPDATE thorny.user_activity '
                           'SET two_months_ago = one_month_ago, one_month_ago = current_month, current_month = $1',
                           timedelta(hours=0))
        print(f"[ACTION] Months successfully switched in all user profiles")

    @staticmethod
    def seconds_until_next_month():
        next_months_date = datetime.now().replace(day=1) + relativedelta(months=1)
        time_until_next_month = next_months_date - datetime.now()
        time_in_seconds = time_until_next_month.total_seconds()
        return time_in_seconds


class Leaderboard:
    @staticmethod
    async def select_activity(ctx, month: datetime):
        if datetime.now() < month:
            month = month.replace(day=1) - relativedelta(years=1, days=1)
        else:
            month = month.replace(day=1) - relativedelta(days=1)
        next_month = month + relativedelta(months=1)
        return await conn.fetch(
            f"""
            SELECT SUM(playtime), thorny.user.user_id 
            FROM thorny.activity 
            JOIN thorny.user ON thorny.user.thorny_user_id = thorny.activity.thorny_user_id
            WHERE connect_time BETWEEN $1 AND $2
            AND playtime IS NOT NULL
            AND thorny.user.guild_id = $3 
            AND thorny.user.active = True
            GROUP BY thorny.user.user_id
            ORDER BY SUM(playtime) DESC
            """,
            month, next_month, ctx.guild.id)

    @staticmethod
    async def select_nugs(ctx):
        return await conn.fetch(f"SELECT user_id, balance FROM thorny.user "
                                f"WHERE thorny.user.guild_id = $1 "
                                f"AND thorny.user.active = True "
                                f"GROUP BY user_id, balance ORDER BY balance DESC", ctx.guild.id)

    @staticmethod
    async def select_treasury():
        return await conn.fetch(f"SELECT kingdom, treasury FROM thorny.kingdoms "
                                f"ORDER BY treasury DESC")


class Kingdom:
    @staticmethod
    async def select_kingdom(kingdom):
        kingdom_dict = await conn.fetchrow("SELECT * "
                                           "FROM thorny.kingdoms "
                                           "WHERE kingdom = $1", kingdom)
        return kingdom_dict

    @staticmethod
    async def update_kingdom(kingdom, section, value):
        try:
            await conn.execute('UPDATE thorny.kingdoms '
                               f'SET {section} = $1 '
                               f'WHERE kingdom = $2', value, kingdom)
        except asyncpg.StringDataRightTruncationError:
            return "length_error"
