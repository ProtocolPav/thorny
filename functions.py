import json
import os
from datetime import datetime, timedelta, date
import asyncio
import discord


# Playtime Functions


def reset_values():
    global openfile, raw_activity, processing_activity, individual_hours, individual_hours_copy, totaling_activity
    openfile = 'abcd'
    raw_activity = []
    processing_activity = []
    individual_hours = []
    individual_hours_copy = []
    totaling_activity = []


def match(item1, item2):
    if int(item2) == int(item1) or int(item2) - int(item1) == 1:
        return True
    else:
        return False


def opendoc_json(month):
    openfile = open(f'../thorny_data/activity_{month}21.json', 'r+')
    raw_activity_local = json.load(openfile)
    return raw_activity_local


def process_json(month):
    global next_log
    raw_activity = opendoc_json(month)
    list_processed = False
    sorted_activity = sorted(raw_activity, key=lambda x: (x['userid'], x['datetime']))

    while not list_processed:
        for log in sorted_activity:
            if sorted_activity[0]['userid'] == log['userid']:
                processing_activity.append(log)
        print(f'[PROCESSING] {processing_activity}')

        for log in processing_activity:
            if processing_activity.index(log) != len(processing_activity) - 1:
                next_log = processing_activity[processing_activity.index(log) + 1]

            # If it's the last log and a CONNECT, it puts it as 2h, as there is no DISCONNECT after
            if processing_activity.index(log) == len(processing_activity) - 1:
                if log['status'] == 'CONNECT':
                    playtime = timedelta(hours=1, minutes=5)
                    append_to_individual_hours(playtime)
                elif log['status'] == 'SET':
                    playtime = timedelta(hours=int(log['datetime']))
                    append_to_individual_hours(playtime)
                else:
                    print("pass")
                    pass

            # If there is no C/DC pair, it sets it as 2h automatically, in case someone 'forgot' to disconnect.
            elif log['status'] == 'CONNECT' and next_log['status'] == 'CONNECT':
                playtime = timedelta(hours=1, minutes=5)
                append_to_individual_hours(playtime)

            elif log['status'] == 'CONNECT' and next_log['status'] == 'DISCONNECT':

                playtime = datetime.strptime(next_log['datetime'], '%Y-%m-%d %H:%M:%S') - \
                           datetime.strptime(log['datetime'], '%Y-%m-%d %H:%M:%S')
                if playtime > timedelta(hours=12):
                    playtime = timedelta(hours=1, minutes=5)
                append_to_individual_hours(playtime)

            elif log['status'] == 'SET':
                playtime = timedelta(hours=int(log['datetime']))
                append_to_individual_hours(playtime)
            else:
                pass

        for item in processing_activity:
            sorted_activity.remove(item)
            if len(sorted_activity) == 0:
                list_processed = True
                individual_hours_copy.append(individual_hours)
        processing_activity.clear()


def total_json(month, ctx_author):
    leaderboard = []
    totaled = False
    name = ''
    while not totaled:
        monthly_playtime = timedelta(hours=0)
        for hour in individual_hours:
            if individual_hours[0]['userid'] == hour['userid']:
                totaling_activity.append(hour)

        # Totals all the individual hours
        for hour in totaling_activity:
            monthly_playtime += hour['playtime']
            name = hour['userid']
        leaderboard.append({"name": name, "time_played": monthly_playtime})

        for item in totaling_activity:
            individual_hours.remove(item)
            if len(individual_hours) == 0:
                totaled = True
        totaling_activity.clear()

    # Sorts and writes the leaderboard into a file
    leaderboard = sorted(leaderboard, key=lambda x: (x['time_played']), reverse=True)
    lb_file = open(f'../thorny_data/leaderboard_{month.lower()}21.json', 'a')
    lb = []
    for rank in leaderboard:
        lb.append(rank)
    lb_file.truncate(0)
    lb_file.seek(0)
    json.dump(lb, lb_file, indent=1, default=str)


def append_to_individual_hours(playtime):
    individual_hours.append({'user': processing_activity[0]['user'],
                             'userid': processing_activity[0]['userid'],
                             'playtime': playtime})
    print(f"{processing_activity[0]['user']} - {playtime}")


def write_log(status: str, datetime, ctx):
    date = datetime.strftime("%B")[0:3]
    ReadFile = open(f'../thorny_data/activity_{date.lower()}21.json', 'a')
    if os.path.getsize(f'../thorny_data/activity_{date.lower()}21.json') == 0:
        ReadFile.write('[]')
    ReadFile = open(f'../thorny_data/activity_{date.lower()}21.json', 'r+')
    file = json.load(ReadFile)
    tempdict = {"status": status,
                "user": f"{ctx.author}",
                "userid": f"{ctx.author.id}",
                "datetime": str(datetime)}
    file.append(tempdict)
    WriteFile = open(f'../thorny_data/activity_{date.lower()}21.json', 'w')
    separated_list_of_event_objects = ',\n'.join(json.dumps(evt) for evt in file)
    WriteFile.write(f'[{separated_list_of_event_objects}]\n')


# Profile Functions


def profile_update(ctx_author, value=None, key1=None, key2=None):
    profile_file = open('../thorny_data/profiles.json', 'r+')
    profile = json.load(profile_file)
    if profile.get(f'{ctx_author.id}') is None:  # User ID search
        profile[str(ctx_author.id)] = {"user": f"{ctx_author}"}

    profile[str(ctx_author.id)]['user'] = f"{ctx_author}"  # Always updates name

    if profile[f'{ctx_author.id}'].get('balance') is None:  # Balance
        profile[str(ctx_author.id)]['balance'] = 25

    if profile[f'{ctx_author.id}'].get('activity') is None:  # Activity
        profile[f'{ctx_author.id}']['activity'] = {}
    if profile[f'{ctx_author.id}']['activity'].get("total") is None:
        profile[f'{ctx_author.id}']['activity']["total"] = "0h00m"
    if profile[f'{ctx_author.id}']['activity'].get("latest_playtime") is None:
        profile[f'{ctx_author.id}']['activity']["latest_playtime"] = "0h00m"
    if profile[f'{ctx_author.id}']['activity'].get("daily_average") is None:
        profile[f'{ctx_author.id}']['activity']["daily_average"] = "0h00m"
    if profile[f'{ctx_author.id}']['activity'].get("current_month") is None:
        profile[f'{ctx_author.id}']['activity']["current_month"] = "0h00m"
    if profile[f'{ctx_author.id}']['activity'].get("1_month_ago") is None:
        profile[f'{ctx_author.id}']['activity']["1_month_ago"] = "0h00m"
    if profile[f'{ctx_author.id}']['activity'].get("2_months_ago") is None:
        profile[f'{ctx_author.id}']['activity']["2_months_ago"] = "0h00m"

    if profile[f'{ctx_author.id}'].get('fields') is None:  # Profile Fields
        profile[f'{ctx_author.id}']['fields'] = {}
    if profile[f'{ctx_author.id}']['fields'].get('slogan') is None:
        profile[f'{ctx_author.id}']['fields']['slogan'] = "Here Goes 5 Word Slogan"
    if profile[f'{ctx_author.id}']['fields'].get('biography') is None:
        profile[f'{ctx_author.id}']['fields']['biography'] = "Here Goes Your Max. 30 Word Bio"
    if profile[f'{ctx_author.id}']['fields'].get('role') is None:
        profile[f'{ctx_author.id}']['fields']['role'] = "Your Role in your kingdom " \
                                                        "(King, Citizen, PoorMan, Council Member, Etc.)"
    if profile[f'{ctx_author.id}']['fields'].get('lore') is None:
        profile[f'{ctx_author.id}']['fields']['lore'] = "Lore about your in-game character here. Max. 30 Words"
    if profile[f'{ctx_author.id}']['fields'].get('wiki') is None:
        profile[f'{ctx_author.id}']['fields']['wiki'] = "https://everthorn.fandom.com/wiki/ Your Featured Page"
    if profile[f'{ctx_author.id}']['fields'].get('town') is None:
        profile[f'{ctx_author.id}']['fields']['town'] = "Your Town"
    if profile[f'{ctx_author.id}']['fields'].get('gamertag') is None:
        profile[f'{ctx_author.id}']['fields']['gamertag'] = "Your Minecraft Gamertag"

    if profile[f'{ctx_author.id}'].get('is_shown') is None:  # Profile Is_Shown
        profile[f'{ctx_author.id}']['is_shown'] = {}
    if profile[f'{ctx_author.id}']['is_shown'].get('information') is None:
        profile[f'{ctx_author.id}']['is_shown']['information'] = True
    if profile[f'{ctx_author.id}']['is_shown'].get('activity') is None:
        profile[f'{ctx_author.id}']['is_shown']['activity'] = True
    if profile[f'{ctx_author.id}']['is_shown'].get('aboutme') is None:
        profile[f'{ctx_author.id}']['is_shown']['aboutme'] = True
    if profile[f'{ctx_author.id}']['is_shown'].get('wiki') is None:
        profile[f'{ctx_author.id}']['is_shown']['wiki'] = True
    if profile[f'{ctx_author.id}']['is_shown'].get('character_story') is None:
        profile[f'{ctx_author.id}']['is_shown']['character_story'] = True

    if profile[f'{ctx_author.id}'].get('inventory') is None:  # Inventory
        profile[f'{ctx_author.id}']['inventory'] = {}
        for slot_number in range(1, 7):  # Inventory Slots
            if profile[f'{ctx_author.id}']['inventory'].get(f'slot{slot_number}') is None:
                profile[f'{ctx_author.id}']['inventory'][f'slot{slot_number}'] = 'Empty'
            if profile[f'{ctx_author.id}']['inventory'].get(f'slot{slot_number}_amount') is None:
                profile[f'{ctx_author.id}']['inventory'][f'slot{slot_number}_amount'] = 0

    if profile[f'{ctx_author.id}'].get('user_level') is None:  # Level
        profile[str(ctx_author.id)]['user_level'] = {"level": 0,
                                                     "xp": 0,
                                                     "required_xp": 0,
                                                     "last_message": "0:0:0"}

    if profile[f'{ctx_author.id}'].get('date_joined') is None:  # Date Joined
        profile[f'{ctx_author.id}']['date_joined'] = ''

    if profile[f'{ctx_author.id}'].get('birthday') is None:  # Birthday
        profile[f'{ctx_author.id}']['birthday'] = {}
    if type(profile[f'{ctx_author.id}']['birthday']) == str:  # Birthday
        profile[f'{ctx_author.id}']['birthday'] = {}
    if profile[f'{ctx_author.id}']['birthday'].get('display') is None:
        profile[f'{ctx_author.id}']['birthday']['display'] = None
    if profile[f'{ctx_author.id}']['birthday'].get('system') is None:
        profile[f'{ctx_author.id}']['birthday']['system'] = None

    if profile[f'{ctx_author.id}']['activity'].get('latest_hour') is not None:
        del profile[f'{ctx_author.id}']['activity']['latest_hour']
    if profile[f'{ctx_author.id}']['activity'].get('latest_minute') is not None:
        del profile[f'{ctx_author.id}']['activity']['latest_minute']

    if key2 is None and key1 is not None:
        profile[f"{ctx_author.id}"][key1] = value
    elif key1 and key2 is not None:
        profile[f"{ctx_author.id}"][key1][key2] = value
    profile_file.truncate(0)
    profile_file.seek(0)
    json.dump(profile, profile_file, indent=3)


def activity_set(ctx_author, value, time_to_add):
    file = open('../thorny_data/profiles.json', 'r+')
    profile_json = json.load(file)

    #  Take information from the value's time and place into variables
    if 'days' in profile_json[f'{ctx_author.id}']['activity'][value]:
        current_days = int(profile_json[f'{ctx_author.id}']['activity'][value].split(' days')[0])
        current_hours = int(profile_json[f'{ctx_author.id}']['activity'][value].split(', ')[1].split('h')[0])
    elif 'day' in profile_json[f'{ctx_author.id}']['activity'][value]:
        current_days = 1
        current_hours = int(profile_json[f'{ctx_author.id}']['activity'][value].split(', ')[1].split('h')[0])
    else:
        current_days = 0
        current_hours = int(profile_json[f'{ctx_author.id}']['activity'][value].split('h')[0])

    current_minutes = int(profile_json[f'{ctx_author.id}']['activity'][value].split('h')[1][:-1])
    #  Take information from time_to_add and place into variables
    hours_to_add = int(time_to_add.split(':')[0])
    minutes_to_add = int(time_to_add.split(':')[1])

    current_time = timedelta(days=current_days, hours=current_hours, minutes=current_minutes)
    playtime_to_add = timedelta(hours=hours_to_add, minutes=minutes_to_add)

    new_total = current_time + playtime_to_add
    formatted_new_total = f"{str(new_total).split(':')[0]}h{str(new_total).split(':')[1]}m"
    return formatted_new_total


def month_change():
    if date.today().day == 1:
        profile_file = open('../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        for player in profile:
            if profile[player]["user"] == "Template":
                pass
            else:
                profile[player]["activity"]["2_months_ago"] = profile[player]["activity"]["1_month_ago"]
                profile[player]["activity"]["1_month_ago"] = profile[player]["activity"]["current_month"]
                profile[player]["activity"]["current_month"] = "0h00m"

        profile_file.truncate(0)
        profile_file.seek(0)
        json.dump(profile, profile_file, indent=3)
    else:
        print(f"{date.today()} is not the 1st of the Month")


def seconds_until_1st():
    date = datetime.now() + timedelta(days=31)
    date_1st = str(date).split(' ')[0][0:7] + "-01" + " " + str(date).split(' ')[1]
    date_1st = datetime.strptime(date_1st, "%Y-%m-%d %H:%M:%S.%f")
    time = date_1st - datetime.now()
    time_seconds = time.total_seconds()
    return time_seconds


async def profile_change_months():
    while True:
        print(f"Month change in {timedelta(seconds=seconds_until_1st())}"
              f" ({datetime.now() + timedelta(seconds=seconds_until_1st())})")
        await asyncio.sleep(seconds_until_1st())
        month_change()
        await asyncio.sleep(60)


async def birthday_announce():
    while True:
        profile_file = open('../thorny_data/profiles.json', 'r+')
        profile = json.load(profile_file)
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for person in profile:
            birthdate = datetime.strptime(profile[person]['birthday']['system'], "%Y-%m-%d %H:%M:%S")
            if str(date)[4:9] == str(birthdate)[4:9]:
                if 1 in str(date)[:4] - str(birthdate)[:4]:
                    await ctx.send(f"<@{person}> {str(date)[:4] - str(birthdate)[:4]}rd Birthday today!")
            else:
                pass
        await asyncio.sleep(86400)  # Needs working on
