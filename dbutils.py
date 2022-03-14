import asyncpg
import asyncpg as pg
import asyncio
from datetime import datetime, timedelta
import json
import discord
from dateutil.relativedelta import relativedelta


async def connection():
    pool = await pg.create_pool(database='postgres', user='postgres', password='p@v3LPlay%MC')
    return pool

conn = asyncio.get_event_loop().run_until_complete(connection())


async def port_user_profiles(ctx):
    profile = json.load(open("../thorny_data/profiles.json", "r"))
    for user in profile:
        print(f"Porting {profile[str(user)]['user']}...")
        total_playtime = profile[str(user)]['activity']['total'].split('h')
        if 'days' in total_playtime[0]:
            total_playtime[0] = total_playtime[0].split(' days, ')
            profile[str(user)]['activity']['total'] = timedelta(days=int(total_playtime[0][0]),
                                                                hours=int(total_playtime[0][1]),
                                                                minutes=int(total_playtime[1][0:2]))
        elif 'day' in total_playtime[0]:
            total_playtime[0] = total_playtime[0].split(' day, ')
            profile[str(user)]['activity']['total'] = timedelta(days=int(total_playtime[0][0]),
                                                                hours=int(total_playtime[0][1]),
                                                                minutes=int(total_playtime[1][0:2]))
        else:
            profile[str(user)]['activity']['total'] = timedelta(hours=int(total_playtime[0]),
                                                                minutes=int(total_playtime[1][0:2]))
        current_playtime = profile[str(user)]['activity']['current_month'].split('h')
        if 'days' in current_playtime[0]:
            current_playtime[0] = current_playtime[0].split(' days, ')
            profile[str(user)]['activity']['current_month'] = timedelta(days=int(current_playtime[0][0]),
                                                                        hours=int(current_playtime[0][1]),
                                                                        minutes=int(current_playtime[1][0:2]))
        elif 'day' in current_playtime[0]:
            current_playtime[0] = current_playtime[0].split(' day, ')
            profile[str(user)]['activity']['current_month'] = timedelta(days=int(current_playtime[0][0]),
                                                                        hours=int(current_playtime[0][1]),
                                                                        minutes=int(current_playtime[1][0:2]))
        else:
            profile[str(user)]['activity']['current_month'] = timedelta(hours=int(current_playtime[0]),
                                                                        minutes=int(current_playtime[1][0:2]))
        last_playtime = profile[str(user)]['activity']['1_month_ago'].split('h')
        if 'days' in last_playtime[0]:
            last_playtime[0] = last_playtime[0].split(' days, ')
            profile[str(user)]['activity']['1_month_ago'] = timedelta(days=int(last_playtime[0][0]),
                                                                      hours=int(last_playtime[0][1]),
                                                                      minutes=int(last_playtime[1][0:2]))
        elif 'day' in last_playtime[0]:
            last_playtime[0] = last_playtime[0].split(' day, ')
            profile[str(user)]['activity']['1_month_ago'] = timedelta(days=int(last_playtime[0][0]),
                                                                      hours=int(last_playtime[0][1]),
                                                                      minutes=int(last_playtime[1][0:2]))
        else:
            profile[str(user)]['activity']['1_month_ago'] = timedelta(hours=int(last_playtime[0]),
                                                                      minutes=int(last_playtime[1][0:2]))

        last_playtime = profile[str(user)]['activity']['2_months_ago'].split('h')
        if 'days' in last_playtime[0]:
            last_playtime[0] = last_playtime[0].split(' days, ')
            profile[str(user)]['activity']['2_months_ago'] = timedelta(days=int(last_playtime[0][0]),
                                                                       hours=int(last_playtime[0][1]),
                                                                       minutes=int(last_playtime[1][0:2]))
        elif 'day' in last_playtime[0]:
            last_playtime[0] = last_playtime[0].split(' day, ')
            profile[str(user)]['activity']['2_months_ago'] = timedelta(days=int(last_playtime[0][0]),
                                                                       hours=int(last_playtime[0][1]),
                                                                       minutes=int(last_playtime[1][0:2]))
        else:
            profile[str(user)]['activity']['2_months_ago'] = timedelta(hours=int(last_playtime[0]),
                                                                       minutes=int(last_playtime[1][0:2]))

        if profile[str(user)].get('kingdom') is not None:
            profile[str(user)]['kingdom'] = profile[str(user)]['kingdom'].capitalize()
        else:
            profile[str(user)]['kingdom'] = None

        if profile[f'{user}'].get('fields') is None:  # Profile Fields
            profile[f'{user}']['fields'] = {}
        if profile[f'{user}']['fields'].get('slogan') is None:
            profile[f'{user}']['fields']['slogan'] = None
        if profile[f'{user}']['fields'].get('biography') is None:
            profile[f'{user}']['fields']['biography'] = None
        if profile[f'{user}']['fields'].get('role') is None:
            profile[f'{user}']['fields']['role'] = None
        if profile[f'{user}']['fields'].get('lore') is None:
            profile[f'{user}']['fields']['lore'] = None
        if profile[f'{user}']['fields'].get('wiki') is None:
            profile[f'{user}']['fields']['wiki'] = None
        if profile[f'{user}']['fields'].get('town') is None:
            profile[f'{user}']['fields']['town'] = None
        if profile[f'{user}']['fields'].get('gamertag') is None:
            profile[f'{user}']['fields']['gamertag'] = None

        if profile[f'{user}'].get('date_joined') is None or profile[f'{user}']['date_joined'] == '':  # Date Joined
            profile[f'{user}']['date_joined'] = None
        else:
            profile[f'{user}']['date_joined'] = datetime.strptime(profile[f'{user}']['date_joined'],
                                                                  "%Y-%m-%d %H:%M:%S")

        if profile[f'{user}'].get('birthday') is None or type(profile[f'{user}']['birthday']) == str:  # Birthday
            profile[f'{user}']['birthday'] = {}
        if profile[f'{user}']['birthday'].get('system') is None:
            profile[f'{user}']['birthday']['system'] = None
        else:
            profile[f'{user}']['birthday']['system'] = datetime.strptime(profile[f'{user}']['birthday']['system'],
                                                                         "%Y-%m-%d %H:%M:%S")
        guild_id = 611008530077712395
        await conn.execute(f'INSERT INTO thorny.user(user_id, username, join_date, birthday, kingdom, balance, '
                           f'guild_id)'
                           f'VALUES($1, $2, $3, $4, $5, $6, $7)',
                           int(user), profile[str(user)]['user'], profile[str(user)]['date_joined'],
                           profile[str(user)]['birthday']['system'], profile[str(user)]['kingdom'],
                           int(profile[str(user)]['balance']), guild_id)

        thorny_id = await conn.fetchrow("SELECT thorny_user_id from thorny.user "
                                        "WHERE user_id = $1", int(user))

        await conn.execute(f'INSERT INTO thorny.user_activity(user_id, total_playtime, current_month, one_month_ago, '
                           f'two_months_ago, thorny_user_id, guild_id) VALUES($1, $2, $3, $4, $5, $6, $7)',
                           int(user), profile[str(user)]['activity']['total'],
                           profile[str(user)]['activity']['current_month'],
                           profile[str(user)]['activity']['1_month_ago'],
                           profile[str(user)]['activity']['2_months_ago'], thorny_id['thorny_user_id'], guild_id)

        delete_these = ['Here Goes 5 Word Slogan', 'A 5 Word Slogan About You', 'Your Minecraft Gamertag',
                        "What's your MC Gamertag?", "Your Town", "WHat town you live in?",
                        "Your Role in your kingdom (King, Citizen, PoorMan, Council Member, Etc.)",
                        "https://everthorn.fandom.com/wiki/ Your Featured Page", "Here Goes Your Max. 30 Word Bio",
                        "About you! Write something fun and interesting! Max. 30 words!",
                        "Lore about your in-game character here. Max. 30 Words",
                        "What's your in game character like? Max. 30 words!", ]
        for field in profile[str(user)]['fields']:
            if profile[str(user)]['fields'][field] in delete_these:
                profile[str(user)]['fields'][field] = None

        await conn.execute(f'INSERT INTO thorny.profile(user_id, slogan, gamertag, town, role, wiki, aboutme, lore,'
                           f'thorny_user_id, guild_id)'
                           f'VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
                           int(user), profile[str(user)]['fields']['slogan'], profile[str(user)]['fields']['gamertag'],
                           profile[str(user)]['fields']['town'],
                           profile[str(user)]['fields']['role'],
                           profile[str(user)]['fields']['wiki'], profile[str(user)]['fields']['biography'],
                           profile[str(user)]['fields']['lore'], thorny_id['thorny_user_id'], guild_id)

        for slot in profile[str(user)]['inventory']:
            if len(profile[str(user)]['inventory']) > 9:
                pass
            else:
                if profile[str(user)]['inventory']['slot1'] is None:
                    pass
                else:
                    if profile[str(user)]['inventory'][slot]['item_id'] != 'empty_00':
                        item = profile[str(user)]['inventory'][slot]['item_id'].split('_')
                        item = f"{item[0]}"
                        await conn.execute('INSERT INTO thorny.inventory(user_id, item_id, item_count, '
                                           'thorny_user_id, guild_id) '
                                           'VALUES($1, $2, $3, $4, $5)',
                                           int(user), item,
                                           int(profile[str(user)]['inventory'][slot]['amount']),
                                           thorny_id['thorny_user_id'], guild_id)
        await conn.execute("INSERT INTO thorny.levels(user_id, thorny_user_id, guild_id) "
                           "VALUES($1, $2, $3)", int(user), thorny_id['thorny_user_id'], guild_id)
        print(f"Porting of {profile[str(user)]['user']} Complete!")


async def port_activity(ctx):
    month = ['oct', 'nov', 'dec']
    await ctx.send(f"Porting September Activity...")
    activity = json.load(open("../thorny_data/activity_sep21.json", "r"))
    sorted_activity = sorted(activity, key=lambda x: (x['userid'], x['date'], x['time']))
    connect_date = None
    user_id = None
    for log in sorted_activity:
        if log['status'] == 'CONNECT' and connect_date is None:
            # This will be used as a second key in addition with the userID to find
            connect_date = datetime.strptime(f"2021 {log['date']} {log['time']}", "%Y %B %d %H:%M:%S")
            user_id = log['userid']
            thorny_id = await conn.fetchrow("SELECT thorny_user_id from thorny.user "
                                            "WHERE user_id = $1", int(user_id))
            guild_id = 611008530077712395
            if thorny_id is not None:
                await conn.execute('INSERT INTO thorny.activity(user_id, connect_time, thorny_user_id, guild_id) '
                                   'VALUES ($1, $2, $3, $4)', int(user_id), connect_date, thorny_id['thorny_user_id'],
                                   guild_id)
            else:
                connect_date = None
                user_id = None

        elif log['status'] == 'CONNECT' and connect_date is not None:
            connect_date = datetime.strptime(f"2021 {log['date']} {log['time']}", "%Y %B %d %H:%M:%S")
            user_id = log['userid']
            playtime = timedelta(hours=1, minutes=5)
            thorny_id = await conn.fetchrow("SELECT thorny_user_id from thorny.user "
                                            "WHERE user_id = $1", int(user_id))
            guild_id = 611008530077712395
            if thorny_id is not None:
                await conn.execute('INSERT INTO thorny.activity(user_id, connect_time, playtime, disconnect_time,'
                                   'thorny_user_id, guild_id) '
                                   'VALUES ($1, $2, $3, $4, $5, $6)', int(user_id), connect_date, playtime,
                                   connect_date,
                                   thorny_id['thorny_user_id'], guild_id)
            connect_date = None
            user_id = None

        elif log['status'] == 'DISCONNECT' and connect_date is not None:
            disconnect_date = datetime.strptime(f"2021 {log['date']} {log['time']}", "%Y %B %d %H:%M:%S")
            playtime = disconnect_date - connect_date
            if playtime >= timedelta(hours=12):
                playtime = timedelta(hours=1, minutes=5)
            await conn.execute("UPDATE thorny.activity "
                               "SET disconnect_time=$1, playtime=$2 "
                               "WHERE user_id=$3 AND connect_time=$4",
                               disconnect_date, playtime, int(user_id), connect_date)
            connect_date = None
            user_id = None
    await ctx.send(f"Porting of September Activity Complete!")
    for mnth in month:
        await ctx.send(f"Porting {mnth} Activity...")
        activity = json.load(open(f"../thorny_data/activity_{mnth}21.json", "r"))
        sorted_activity = sorted(activity, key=lambda x: (x['userid'], x['datetime']))
        connect_date = None
        user_id = None
        for log in sorted_activity:
            if log['status'] == 'CONNECT' and connect_date is None:
                # This will be used as a second key in addition with the userID to find
                connect_date = datetime.strptime(log['datetime'], "%Y-%m-%d %H:%M:%S")
                user_id = log['userid']
                thorny_id = await conn.fetchrow("SELECT thorny_user_id from thorny.user "
                                                "WHERE user_id = $1", int(user_id))
                guild_id = 611008530077712395
                if thorny_id is not None:
                    await conn.execute('INSERT INTO thorny.activity(user_id, connect_time, thorny_user_id, guild_id) '
                                       'VALUES ($1, $2, $3, $4)', int(user_id), connect_date,
                                       thorny_id['thorny_user_id'],
                                       guild_id)
                else:
                    connect_date = None
                    user_id = None

            elif log['status'] == 'CONNECT' and connect_date is not None:
                connect_date = datetime.strptime(log['datetime'], "%Y-%m-%d %H:%M:%S")
                user_id = log['userid']
                playtime = timedelta(hours=1, minutes=5)
                thorny_id = await conn.fetchrow("SELECT thorny_user_id from thorny.user "
                                                "WHERE user_id = $1", int(user_id))
                guild_id = 611008530077712395
                if thorny_id is not None:
                    await conn.execute('INSERT INTO thorny.activity(user_id, connect_time, playtime, disconnect_time,'
                                       'thorny_user_id, guild_id) '
                                       'VALUES ($1, $2, $3, $4, $5, $6)', int(user_id), connect_date, playtime,
                                       connect_date,
                                       thorny_id['thorny_user_id'], guild_id)
                connect_date = None
                user_id = None

            elif log['status'] == 'DISCONNECT' and connect_date is not None:
                disconnect_date = datetime.strptime(log['datetime'], "%Y-%m-%d %H:%M:%S")
                playtime = disconnect_date - connect_date
                if playtime >= timedelta(hours=12):
                    playtime = timedelta(hours=1, minutes=5)
                await conn.execute("UPDATE thorny.activity "
                                   "SET disconnect_time=$1, playtime=$2 "
                                   "WHERE user_id=$3 AND connect_time=$4",
                                   disconnect_date, playtime, int(user_id), connect_date)
                connect_date = None
                user_id = None
        await ctx.send(f"Porting of {mnth} Activity Complete!")


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
    await conn.execute("CREATE TABLE thorny.strikes("
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
        res = await conn.fetchrow("SELECT * FROM thorny.activity WHERE user_id = $1 ORDER BY connect_time DESC",
                                   user_id)
        return ActivityData(connect_time=res.connect_time)

    @staticmethod
    async def select_online():
        return await conn.fetch("SELECT * FROM thorny.activity WHERE disconnect_time is NULL AND connect_time > $1 "
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
    async def select_activity(month: datetime):
        if datetime.now() < month:
            month = month.replace(year=datetime.now().year - 1)
            year = datetime.now().year - 1
        else:
            year = datetime.now().year
        next_month = month.month + 1
        if next_month == 13:
            next_month = 1
            year = datetime.now().year
        return await conn.fetch(
            f"""
            SELECT SUM(playtime), user_id 
            FROM thorny.activity 
            WHERE connect_time BETWEEN $1 AND $2
            GROUP BY user_id 
            ORDER BY SUM(playtime) DESC
            """,
            month.replace(day=1, hour=0, minute=0, second=0, microsecond=0),
            month.replace(year=year, month=next_month, day=1, hour=0, minute=0, second=0, microsecond=0))

    @staticmethod
    async def select_nugs():
        return await conn.fetch(f"SELECT user_id, balance FROM thorny.user "
                                f"GROUP BY user_id, balance ORDER BY balance DESC")


class Profile:
    @staticmethod
    async def select_profile(user_id):
        return await conn.fetchrow(f"SELECT * FROM (((thorny.user "
                                   f"INNER JOIN thorny.profile ON thorny.profile.user_id = thorny.user.user_id) "
                                   f"INNER JOIN thorny.levels ON thorny.levels.user_id = thorny.user.user_id) "
                                   f"INNER JOIN thorny.user_activity ON "
                                   f"thorny.user_activity.user_id = thorny.user.user_id)"
                                   f"WHERE thorny.user.user_id = $1", user_id)

    @staticmethod
    async def update_profile(user_id, section, value):
        availabe_sections = ['slogan', 'gamertag', 'town', 'role', 'wiki', 'aboutme', 'lore']
        if section.lower() in availabe_sections:
            try:
                await conn.execute('UPDATE thorny.profile '
                                   f'SET {section} = $1 '
                                   f'WHERE user_id = $2', value, user_id)
            except asyncpg.StringDataRightTruncationError:
                return "length_error"
        else:
            return "section_error"

    @staticmethod
    async def update_toggle(user_id, section):
        availabe_sections = ['information', 'activity', 'wiki', 'aboutme', 'lore']
        if section.lower() in availabe_sections:
            await conn.execute('UPDATE thorny.profile '
                               f'SET {section}_shown = NOT {section}_shown '
                               f'WHERE user_id = $1', user_id)
        else:
            return "section_error"

    @staticmethod
    async def insert_strike(user_id, reason, cm_id):
        strike_id = await conn.fetchrow('SELECT strike_id '
                                        'FROM thorny.strikes '
                                        'ORDER BY strike_id DESC')
        await conn.execute('INSERT INTO thorny.strikes '
                           'VALUES($1, $2, $3, $4)',
                           strike_id[0] + 1, user_id, reason, cm_id)
        return strike_id[0] + 1

    @staticmethod
    async def delete_strike(strike_id):
        await conn.execute("DELETE FROM thorny.strikes "
                           "WHERE strike_id = $1", strike_id)
        return True


class Kingdom:
    @staticmethod
    async def select_kingdom(kingdom):
        kingdom_dict = await conn.fetchrow("SELECT * "
                                           "FROM thorny.kingdoms "
                                           "WHERE kingdom = $1", kingdom)
        return kingdom_dict

    @staticmethod
    async def update_kingdom(kingdom, section, value):
        availabe_sections = ['slogan', 'capital', 'town_count', 'border_type', 'gov_type', 'description',
                             'alliances', 'lore']
        if section.lower() in availabe_sections:
            try:
                await conn.execute('UPDATE thorny.kingdoms '
                                   f'SET {section} = $1 '
                                   f'WHERE kingdom = $2', value, kingdom)
            except asyncpg.StringDataRightTruncationError:
                return "length_error"
        else:
            return "section_error"
