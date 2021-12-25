import psycopg2 as ps
from datetime import datetime, timedelta
import discord

connection = ps.connect(dbname='postgres', user='postgres', password='***REMOVED***')
cursor = connection.cursor()

""" These are one-time use commands """


def port_user_profiles():
    conn = ps.connect(dbname='postgres', user='postgres', password='***REMOVED***')
    cur = connection.cursor()

    profile = json.load(open("thorny_data/profiles.json", "r"))
    for user in profile:
        playtime = profile[str(user)]['activity']['total'].split('h')
        if 'days' in playtime[0]:
            playtime[0] = playtime[0].split(' days, ')
            profile[str(user)]['activity']['total'] = timedelta(days=int(playtime[0][0]), hours=int(playtime[0][1]),
                                                                minutes=int(playtime[1][0:2]))
        playtime2 = profile[str(user)]['activity']['current_month'].split('h')
        if 'days' in playtime2[0]:
            playtime2[0] = playtime2[0].split(' days, ')
            profile[str(user)]['activity']['current_month'] = timedelta(days=int(playtime2[0][0]),
                                                                        hours=int(playtime2[0][1]),
                                                                        minutes=int(playtime2[1][0:2]))
        playtime3 = profile[str(user)]['activity']['1_month_ago'].split('h')
        if 'days' in playtime3[0]:
            playtime3[0] = playtime3[0].split(' days, ')
            profile[str(user)]['activity']['1_month_ago'] = timedelta(days=int(playtime3[0][0]),
                                                                      hours=int(playtime3[0][1]),
                                                                      minutes=int(playtime3[1][0:2]))
        playtime3 = profile[str(user)]['activity']['2_months_ago'].split('h')
        if 'days' in playtime3[0]:
            playtime3[0] = playtime3[0].split(' days, ')
            profile[str(user)]['activity']['2_months_ago'] = timedelta(days=int(playtime3[0][0]),
                                                                       hours=int(playtime3[0][1]),
                                                                       minutes=int(playtime3[1][0:2]))
        if profile[str(user)].get('kingdom') is not None:
            profile[str(user)]['kingdom'] = profile[str(user)]['kingdom'].capitalize()
        else:
            profile[str(user)]['kingdom'] = None

        if profile[str(user)].get('balance') is None:  # Balance
            profile[str(user)]['balance'] = 30

        if profile[f'{user}'].get('kingdom') is None:  # Kingdom
            profile[str(user)]['kingdom'] = None

        if profile[f'{user}'].get('activity') is None:  # Activity
            profile[f'{user}']['activity'] = {}
        if profile[f'{user}']['activity'].get("total") is None:
            profile[f'{user}']['activity']["total"] = "0h00m"
        if profile[f'{user}']['activity'].get("latest_playtime") is None:
            profile[f'{user}']['activity']["latest_playtime"] = "0h00m"
        if profile[f'{user}']['activity'].get("daily_average") is None:
            profile[f'{user}']['activity']["daily_average"] = "0h00m"
        if profile[f'{user}']['activity'].get("current_month") is None:
            profile[f'{user}']['activity']["current_month"] = "0h00m"
        if profile[f'{user}']['activity'].get("1_month_ago") is None:
            profile[f'{user}']['activity']["1_month_ago"] = "0h00m"
        if profile[f'{user}']['activity'].get("2_months_ago") is None:
            profile[f'{user}']['activity']["2_months_ago"] = "0h00m"

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

        if profile[f'{user}'].get('date_joined') is None:  # Date Joined
            profile[f'{user}']['date_joined'] = None

        elif profile[f'{user}']['date_joined'] == '':  # Date Joined
            profile[f'{user}']['date_joined'] = None

        if profile[f'{user}'].get('birthday') is None:  # Birthday
            profile[f'{user}']['birthday'] = {}
        if type(profile[f'{user}']['birthday']) == str:  # Birthday
            profile[f'{user}']['birthday'] = {}
        if profile[f'{user}']['birthday'].get('system') is None:
            profile[f'{user}']['birthday']['system'] = None

        cur.execute(f'INSERT INTO thorny.user(user_id, username, join_date, birthday, kingdom, balance)'
                    f'VALUES(%s, %s, %s, %s, %s, %s)',
                    (user, profile[str(user)]['user'], profile[str(user)]['date_joined'],
                     profile[str(user)]['birthday']['system'], profile[str(user)]['kingdom'],
                     profile[str(user)]['balance']))
        cur.execute(f'INSERT INTO thorny.user_activity(user_id, total_playtime, current_month, "1_month_ago", '
                    f'"2_months_ago")'
                    'VALUES(%s, %s, %s, %s, %s)', (user, profile[str(user)]['activity']['total'],
                                                   profile[str(user)]['activity']['current_month'],
                                                   profile[str(user)]['activity']['1_month_ago'],
                                                   profile[str(user)]['activity']['2_months_ago']))
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
        cur.execute(f'INSERT INTO thorny.profile(user_id, slogan, gamertag, town, role, wiki, aboutme, lore)'
                    f'VALUES(%s, %s, %s, %s, %s, %s, %s, %s)',
                    (user, profile[str(user)]['fields']['slogan'], profile[str(user)]['fields']['gamertag'],
                     profile[str(user)]['fields']['town'], profile[str(user)]['fields']['role'],
                     profile[str(user)]['fields']['wiki'], profile[str(user)]['fields']['biography'],
                     profile[str(user)]['fields']['lore']))
        for slot in profile[str(user)]['inventory']:
            if len(profile[str(user)]['inventory']) > 9:
                pass
            else:
                if profile[str(user)]['inventory']['slot1'] is None:
                    pass
                else:
                    if profile[str(user)]['inventory'][slot]['item_id'] != 'empty_00':
                        cur.execute('INSERT INTO thorny.inventory(user_id, item_id, item_count) '
                                    'VALUES(%s, %s, %s)',
                                    (user, profile[str(user)]['inventory'][slot]['item_id'],
                                     profile[str(user)]['inventory'][slot]['amount']))
        conn.commit()


def port_activity():
    conn = ps.connect(dbname='postgres', user='postgres', password='***REMOVED***')
    cur = connection.cursor()

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
            cur.execute('INSERT INTO thorny.activity(user_id, connect_time) '
                        'VALUES (%s, %s)', (user_id, connect_date))

        elif log['status'] == 'CONNECT' and connect_date is not None:
            connect_date = datetime.strptime(f"2021 {log['date']} {log['time']}", "%Y %B %d %H:%M:%S")
            user_id = log['userid']
            cur.execute('INSERT INTO thorny.activity(user_id, connect_time) '
                        'VALUES (%s, %s)', (user_id, connect_date))
            connect_date = None
            user_id = None

        elif log['status'] == 'DISCONNECT' and connect_date is not None:
            disconnect_date = datetime.strptime(f"2021 {log['date']} {log['time']}", "%Y %B %d %H:%M:%S")
            playtime = disconnect_date - connect_date
            cur.execute("UPDATE thorny.activity "
                        "SET disconnect_time=%s, playtime=%s "
                        "WHERE user_id=%s AND connect_time=%s", (disconnect_date, playtime, user_id, connect_date))
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
                cur.execute('INSERT INTO thorny.activity(user_id, connect_time) '
                            'VALUES (%s, %s)', (user_id, connect_date))

            elif log['status'] == 'CONNECT' and connect_date is not None:
                connect_date = datetime.strptime(log['datetime'], "%Y-%m-%d %H:%M:%S")
                user_id = log['userid']
                cur.execute('INSERT INTO thorny.activity(user_id, connect_time) '
                            'VALUES (%s, %s)', (user_id, connect_date))
                connect_date = None
                user_id = None

            elif log['status'] == 'DISCONNECT' and connect_date is not None:
                disconnect_date = datetime.strptime(log['datetime'], "%Y-%m-%d %H:%M:%S")
                playtime = disconnect_date - connect_date
                cur.execute("UPDATE thorny.activity "
                            "SET disconnect_time=%s, playtime=%s "
                            "WHERE user_id=%s AND connect_time=%s", (disconnect_date, playtime, user_id, connect_date))
                connect_date = None
                user_id = None
    conn.commit()
