import json
import os


def reset_values():
    global openfile, raw_activity, processing_activity, individual_hours, individual_hours_copy, totaling_activity
    openfile = 'abcd'
    raw_activity = []
    processing_activity = []
    individual_hours = []
    individual_hours_copy = []
    totaling_activity = []


def append_to_individual_hours(hrs_played, min_played):
    individual_hours.append({'user': processing_activity[0]['user'],
                             'userid': processing_activity[0]['userid'],
                             'hours': hrs_played,
                             'minutes': min_played})
    print(f"{processing_activity[0]['user']} - {hrs_played}h{min_played}m")


def write_log(status: str, current_time: str, ctx):
    ReadFile = open(f'text files/activity_{current_time[0:3].lower()}21.json', 'a')
    if os.path.getsize(f'text files/activity_{current_time[0:3].lower()}21.json') == 0:
        ReadFile.write('[]')
    ReadFile = open(f'text files/activity_{current_time[0:3].lower()}21.json', 'r+')
    file = json.load(ReadFile)
    write_time = current_time.split(',')
    tempdict = {"status": status,
                "user": f"{ctx.author}",
                "userid": f"{ctx.author.id}",
                "date": f"{write_time[0]}",
                "time": f"{write_time[2][1:9]}"}
    file.append(tempdict)
    WriteFile = open(f'text files/activity_{current_time[0:3].lower()}21.json', 'w')
    separated_list_of_event_objects = ',\n'.join(json.dumps(evt) for evt in file)
    WriteFile.write(f'[{separated_list_of_event_objects}]\n')


def find_user_index(lst, key, value):
    for index, dic in enumerate(lst):
        if dic[key] == value:
            return index
    return None


def profile_update(ctx_author, value=None, key1=None, key2=None):
    profile_file = open('text files/profiles.json', 'r+')
    profile = json.load(profile_file)
    if str(ctx_author.id) not in profile:
        profile[str(ctx_author.id)] = ({"user": f"{ctx_author}",
                                        "balance": 25,
                                        "activity": {
                                            "total": 0,
                                            "latest_hour": 0,
                                            "latest_minute": 0,
                                            "daily_average": None,
                                            "current_month": 0,
                                            "1_month_ago": 0,
                                            "2_months_ago": 0
                                        },
                                        "inventory": {
                                            "slot1": None,
                                            "slot2": None,
                                            "slot3": None,
                                            "slot4": None,
                                            "slot5": None,
                                            "slot6": None
                                        },
                                        "user_level": {
                                            "level": 0,
                                            "xp": 0,
                                            "required_xp": 0,
                                            "last_message": "0:0:0"
                                        },
                                        "date_joined": None
                                        })
    if key2 is None and key1 is not None:
        profile[f"{ctx_author.id}"][key1] = value
    elif value and key1 and key2 is not None:
        profile[f"{ctx_author.id}"][key1][key2] = value
    profile_file.truncate(0)
    profile_file.seek(0)
    json.dump(profile, profile_file, indent=3)


def match(item1, item2):
    if int(item2) == int(item1) or int(item2) - int(item1) == 1:
        return True
    else:
        return False


def opendoc_json(month):
    openfile = open(f'text files/activity_{month}21.json', 'r+')
    raw_activity_local = json.load(openfile)
    return raw_activity_local


def process_json(month):
    global next_log
    raw_activity = opendoc_json(month)
    list_processed = False
    sorted_activity = sorted(raw_activity, key=lambda x: (x['userid'], x['date'], x['time']))

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
                    hrs_played = 1
                    min_played = 5
                    append_to_individual_hours(hrs_played, min_played)
                else:
                    print("pass")
                    pass

            # If there is no C/DC pair, it sets it as 2h automatically, in case someone 'forgot' to disconnect.
            elif log['status'] == 'CONNECT' and next_log['status'] == 'CONNECT':
                hrs_played = 1
                min_played = 5
                append_to_individual_hours(hrs_played, min_played)

            elif log['status'] == 'CONNECT' and next_log['status'] == 'DISCONNECT':
                log_times = [int(log['time'][0:2]), int(next_log['time'][0:2]),
                             int(log['time'][3:5]), int(next_log['time'][3:5])]

                hrs_played = log_times[1] - log_times[0]
                min_played = log_times[3] - log_times[2]
                if hrs_played < 0:
                    hrs_played += 24
                if hrs_played >= 12:
                    hrs_played = 2
                if min_played < 0:
                    min_played += 60
                append_to_individual_hours(hrs_played, min_played)

            elif log['status'] == 'SET':
                hrs_played = int(log['time'])
                append_to_individual_hours(hrs_played, 0)
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
        monthly_hours = 0
        monthly_minutes = 0
        for hour in individual_hours:
            if individual_hours[0]['userid'] == hour['userid']:
                totaling_activity.append(hour)

        # Totals all the individual hours
        for hour in totaling_activity:
            monthly_hours += hour['hours']
            monthly_minutes += hour['minutes']
            name = hour['userid']
        if monthly_minutes > 59:
            monthly_hours += round(monthly_minutes / 60)
        if monthly_hours < 1:
            monthly_hours = monthly_minutes / 100
        leaderboard.append({"name": name, "time_played": monthly_hours})

        for item in totaling_activity:
            individual_hours.remove(item)
            if len(individual_hours) == 0:
                totaled = True
        totaling_activity.clear()

    # Sorts and writes the leaderboard into a file
    leaderboard = sorted(leaderboard, key=lambda x: (x['time_played']), reverse=True)
    lb_file = open(f'text files/leaderboard_{month.lower()}21.json', 'a')
    lb = []
    for rank in leaderboard:
        lb.append(rank)
    lb_file.truncate(0)
    lb_file.seek(0)
    json.dump(lb, lb_file, indent=1)


def statistics_json():
    pass


if __name__ == 'b__main__':
    opendoc('aug')
    process()
    total('aug')

if __name__ == '__main__':
    reset_values()
    process_json('aug')
    total_json('aug')
