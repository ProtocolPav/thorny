import asyncpg as pg
import asyncio
from datetime import datetime, timedelta
import json
import discord

# connection = ps.connect(dbname='postgres', user='postgres', password='p@v3LPlay%MC')
# cursor = connection.cursor()

""" Needs reworking to asyncpg. Test in school.py first """


async def connection():
    pool = await pg.create_pool(database='postgres', user='postgres', password='p@v3LPlay%MC')
    return pool


conn = asyncio.get_event_loop().run_until_complete(connection())


async def port_user_profiles():
    conn = await pg.connect(database='postgres', user='postgres', password='p@v3LPlay%MC')

    profile = json.load(open("../thorny_data/profiles.json", "r"))
    for user in profile:
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

        await conn.execute(f'INSERT INTO thorny.user(user_id, username, join_date, birthday, kingdom, balance)'
                           f'VALUES($1, $2, $3, $4, $5, $6)',
                           int(user), profile[str(user)]['user'], profile[str(user)]['date_joined'],
                           profile[str(user)]['birthday']['system'], profile[str(user)]['kingdom'],
                           int(profile[str(user)]['balance']))

        await conn.execute(f'INSERT INTO thorny.user_activity(user_id, total_playtime, current_month, "1_month_ago", '
                           f'"2_months_ago") VALUES($1, $2, $3, $4, $5)',
                           int(user), profile[str(user)]['activity']['total'],
                           profile[str(user)]['activity']['current_month'],
                           profile[str(user)]['activity']['1_month_ago'],
                           profile[str(user)]['activity']['2_months_ago'])

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

        await conn.execute(f'INSERT INTO thorny.profile(user_id, slogan, gamertag, town, role, wiki, aboutme, lore)'
                           f'VALUES($1, $2, $3, $4, $5, $6, $7, $8)',
                           int(user), profile[str(user)]['fields']['slogan'], profile[str(user)]['fields']['gamertag'],
                           profile[str(user)]['fields']['town'].capitalize(),
                           profile[str(user)]['fields']['role'].capitalize(),
                           profile[str(user)]['fields']['wiki'], profile[str(user)]['fields']['biography'],
                           profile[str(user)]['fields']['lore'])

        for slot in profile[str(user)]['inventory']:
            if len(profile[str(user)]['inventory']) > 9:
                pass
            else:
                if profile[str(user)]['inventory']['slot1'] is None:
                    pass
                else:
                    if profile[str(user)]['inventory'][slot]['item_id'] != 'empty_00':
                        item = '_'.split(profile[str(user)]['inventory'][slot]['item_id'])
                        item = f"{item[0]}_{item[1][1]}"
                        await conn.execute('INSERT INTO thorny.inventory(user_id, item_id, item_count) '
                                           'VALUES($1, $2, $3)',
                                           int(user), item,
                                           int(profile[str(user)]['inventory'][slot]['amount']))


async def port_activity():
    conn = await pg.connect(database='postgres', user='postgres', password='p@v3LPlay%MC')

    month = ['oct', 'nov', 'dec']
    activity = json.load(open("thorny_data/activity_sep21.json", "r"))
    sorted_activity = sorted(activity, key=lambda x: (x['userid'], x['date'], x['time']))
    connect_date = None
    user_id = None
    for log in sorted_activity:
        if log['status'] == 'CONNECT' and connect_date is None:
            # This will be used as a second key in addition with the userID to find
            connect_date = datetime.strptime(f"2021 {log['date']} {log['time']}", "%Y %B %d %H:%M:%S")
            user_id = log['userid']
            await conn.execute('INSERT INTO thorny.activity(user_id, connect_time) '
                               'VALUES ($1, $2)', int(user_id), connect_date)

        elif log['status'] == 'CONNECT' and connect_date is not None:
            connect_date = datetime.strptime(f"2021 {log['date']} {log['time']}", "%Y %B %d %H:%M:%S")
            user_id = log['userid']
            await conn.execute('INSERT INTO thorny.activity(user_id, connect_time) '
                               'VALUES ($1, $2)', int(user_id), connect_date)
            connect_date = None
            user_id = None

        elif log['status'] == 'DISCONNECT' and connect_date is not None:
            disconnect_date = datetime.strptime(f"2021 {log['date']} {log['time']}", "%Y %B %d %H:%M:%S")
            playtime = disconnect_date - connect_date
            await conn.execute("UPDATE thorny.activity "
                               "SET disconnect_time=$1, playtime=$2 "
                               "WHERE user_id=$3 AND connect_time=$4",
                               disconnect_date, playtime, int(user_id), connect_date)
            connect_date = None
            user_id = None
    for mnth in month:
        activity = json.load(open(f"thorny_data/activity_{mnth}21.json", "r"))
        sorted_activity = sorted(activity, key=lambda x: (x['userid'], x['datetime']))
        connect_date = None
        user_id = None
        for log in sorted_activity:
            if log['status'] == 'CONNECT' and connect_date is None:
                # This will be used as a second key in addition with the userID to find
                connect_date = datetime.strptime(log['datetime'], "%Y-%m-%d %H:%M:%S")
                user_id = log['userid']
                await conn.execute('INSERT INTO thorny.activity(user_id, connect_time) '
                                   'VALUES ($1, $2)', int(user_id), connect_date)

            elif log['status'] == 'CONNECT' and connect_date is not None:
                connect_date = datetime.strptime(log['datetime'], "%Y-%m-%d %H:%M:%S")
                user_id = log['userid']
                await conn.execute('INSERT INTO thorny.activity(user_id, connect_time) '
                                   'VALUES ($1, $2)', int(user_id), connect_date)
                connect_date = None
                user_id = None

            elif log['status'] == 'DISCONNECT' and connect_date is not None:
                disconnect_date = datetime.strptime(log['datetime'], "%Y-%m-%d %H:%M:%S")
                playtime = disconnect_date - connect_date
                await conn.execute("UPDATE thorny.activity "
                                   "SET disconnect_time=$1, playtime=$2 "
                                   "WHERE user_id=$3 AND connect_time=$4",
                                   disconnect_date, playtime, int(user_id), connect_date)
                connect_date = None
                user_id = None


async def condition_select(table, column, condition, condition_req):
    return await conn.fetch(f"SELECT {column} FROM thorny.{table} WHERE {condition}=$1", condition_req)


async def simple_select(table, column):
    return await conn.fetch(f"SELECT {column} FROM thorny.{table}")


async def simple_update(table, column, new_val, condition, condition_requirement):
    await conn.execute(f"UPDATE thorny.{table} "
                       f"SET {column}=$1"
                       f"WHERE {condition}=$2", new_val, condition_requirement)


class Inventory:
    @staticmethod
    async def select(item_id, user_id):
        return await conn.fetchrow(f"SELECT * FROM thorny.inventory WHERE user_id=$1 AND item_id=$2", user_id, item_id)

    @staticmethod
    async def delete(item_id, user_id):
        await conn.execute("DELETE FROM thorny.inventory WHERE user_id=$1 AND item_id =$2", user_id, item_id)

    @staticmethod
    async def insert(item_id, item_count, user_id):
        await conn.execute(f"INSERT INTO thorny.inventory(user_id, item_id, item_count)"
                           f"VALUES($1, $2, $3)", user_id, item_id, item_count)

    @staticmethod
    async def update(item_id, item_count, user_id):
        await conn.execute(f"UPDATE thorny.inventory SET item_count=$1 WHERE user_id=$2 AND item_id=$3",
                           item_count, user_id, item_id)

    @staticmethod
    async def get_item_type(item):
        try:
            int(item)
        except ValueError:
            return await conn.fetchrow(f"SELECT * FROM thorny.item_type WHERE item_id=$1 OR friendly_id=$1",
                                       item)
        else:
            return await conn.fetchrow(f"SELECT * FROM thorny.item_type WHERE unique_id=$1",
                                       int(item))

    @staticmethod
    async def update_item_price(item, price):
        try:
            int(item)
        except ValueError:
            await conn.execute(f"UPDATE thorny.item_type SET item_cost = $2 WHERE item_id=$1 OR friendly_id=$1",
                               item, int(price))
            return True
        else:
            await conn.execute(f"UPDATE thorny.item_type SET item_cost = $2 WHERE unique_id=$1",
                               int(item), int(price))
            return True
