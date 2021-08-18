import json

OpenFile = 'abcd'
rawActivity = []
processingActivity = []
individualHours = []
totalingActivity = []


def reset_values():
    rawActivity.clear()
    processingActivity.clear()
    individualHours.clear()
    totalingActivity.clear()


def opendoc(month):
    openfile = open(f'text files/activity_{month}21.txt', 'r')
    for line in openfile:
        field = line.split(',')
        if len(field) > 1:
            status = field[0]
            date = field[1]
            time = field[3]
            player = field[4]
            playerid = field[5]
            rawActivity.append(
                [status, player[1:len(player)], date[1:len(date)], time[1:len(time)], playerid[1:len(playerid)]])
        else:
            field.remove(line)
    # Opens the file, adds fields into the raw list for it to begin processing


def opendoc_json(month):
    openfile = open(f'text files/activity_{month}21.json', 'r+')
    raw_activity_local = json.load(openfile)
    return raw_activity_local


def matching(item1, item2):
    if int(item2) == int(item1) or int(item2) - int(item1) == 1:
        return True
    else:
        return False


def process():
    hoursPlayed = 0
    minPlayed = 0
    listprocessed = False
    sortedActivity = sorted(rawActivity, key=lambda x: (x[1], x[2], x[3]))
    # Sorts the raw list. Sorts first by names, then by date and time.
    while not listprocessed:
        for log in sortedActivity:
            if sortedActivity[0][1] == log[1]:
                processingActivity.append(log)
        # Adds all logs with the same name into a separate list for processing
        print(f'[PROCESSING] {processingActivity}')
        for log in processingActivity:
            if processingActivity.index(log) == len(processingActivity) - 1:
                if log[0] == 'CONNECT':
                    hoursPlayed = 2
                    minPlayed = 0
                    individualHours.append([processingActivity[0][1], hoursPlayed, minPlayed])
                    print(f"{processingActivity[0][1]} - {hoursPlayed}h{minPlayed}m")
                else:
                    print("pass")
                    pass
            # Checks if the log is the last item in the list, if it is then it passes.
            # If it's the last one and a CONNECT, it puts it as 2h
            elif log[0] == 'CONNECT' and processingActivity[processingActivity.index(log) + 1][0] == 'DISCONNECT':
                cHour = int(log[3][0:2])
                cMin = int(log[3][3:5])
                dcHour = int(processingActivity[processingActivity.index(log) + 1][3][0:2])
                dcMin = int(processingActivity[processingActivity.index(log) + 1][3][3:5])

                hoursPlayed = dcHour - cHour
                minPlayed = dcMin - cMin
                if hoursPlayed < 0:
                    hoursPlayed += 24
                if hoursPlayed >= 14:
                    hoursPlayed = 2
                if minPlayed < 0:
                    minPlayed += 60
                individualHours.append([processingActivity[0][1], hoursPlayed, minPlayed])
                print(f"{processingActivity[0][1]} - {hoursPlayed}h{minPlayed}m")
            # Checks if the current log is CONNECT and if the log next to it is DISCONNECT, calculates time.
            elif log[0] == 'CONNECT' and processingActivity[processingActivity.index(log) + 1][0] == 'CONNECT':
                hoursPlayed = 2
                minPlayed = 0
                individualHours.append([processingActivity[0][1], hoursPlayed, minPlayed])
                print(f"{processingActivity[0][1]} - {hoursPlayed}h{minPlayed}m")
            else:
                pass
        # If there is no C/DC pair, it sets it as 2h automatically, in case someone 'forgot' to disconnect.
        for item in processingActivity:
            sortedActivity.remove(item)
        processingActivity.clear()
        if len(sortedActivity) == 0:
            listprocessed = True
    # Removes the processed items from the processing list. If there's 0 items, then the flag is raised.


def process_json():
    list_processed = False
    sortedActivity = sorted(rawActivity, key=lambda x: (x['userid'], x['date'], x['time']))
    # Sorts the raw list. Sorts first by names, then by date and time.
    while not list_processed:
        for log in sortedActivity:
            if sortedActivity[0]['userid'] == log['userid']:
                processingActivity.append(log)
        # Adds all logs with the same userid into a separate dict for processing
        print(f'[PROCESSING] {processingActivity}')
        for log in processingActivity:
            if processingActivity.index(log) == len(processingActivity) - 1:
                if log['status'] == 'CONNECT':
                    hrs_played = 2
                    min_played = 0
                    individualHours.append({'user': processingActivity[0]['user'],
                                            'userid': processingActivity[0]['userid'],
                                            'hours': hrs_played,
                                            'minutes': min_played})
                    print(f"{processingActivity[0]['user']} - {hrs_played}h{min_played}m")
                else:
                    print("pass")
                    pass
            # Checks if the log is the last item in the list, if it is then it passes.
            # If it's the last one and a CONNECT, it puts it as 2h
            elif log['status'] == 'CONNECT' and processingActivity[processingActivity.index(log)+1]['status'] == 'DISCONNECT':
                cHour = int(log['time'][0:2])
                cMin = int(log['time'][3:5])
                dcHour = int(processingActivity[processingActivity.index(log) + 1]['time'][0:2])
                dcMin = int(processingActivity[processingActivity.index(log) + 1]['time'][3:5])

                hrs_played = dcHour - cHour
                min_played = dcMin - cMin
                if hrs_played < 0:
                    hrs_played += 24
                if hrs_played >= 14:
                    hrs_played = 2
                if min_played < 0:
                    min_played += 60
                individualHours.append({'user': processingActivity[0]['user'],
                                        'userid': processingActivity[0]['userid'],
                                        'hours': hrs_played,
                                        'minutes': min_played})
                print(f"{processingActivity[0]['user']} - {hrs_played}h{min_played}m")
            # Checks if the current log is CONNECT and if the log next to it is DISCONNECT, calculates time.
            elif log['status'] == 'CONNECT' and processingActivity[processingActivity.index(log) + 1]['status'] == 'CONNECT':
                hrs_played = 2
                min_played = 0
                individualHours.append({'user': processingActivity[0]['user'],
                                        'userid': processingActivity[0]['userid'],
                                        'hours': hrs_played,
                                        'minutes': min_played})
                print(f"{processingActivity[0]['user']} - {hrs_played}h{min_played}m")
            else:
                pass
        # If there is no C/DC pair, it sets it as 2h automatically, in case someone 'forgot' to disconnect.
        for item in processingActivity:
            sortedActivity.remove(item)
        processingActivity.clear()
        if len(sortedActivity) == 0:
            list_processed = True
    # Removes the processed items from the processing list. If there's 0 items, then the flag is raised.


def total(month):
    leaderboard = []
    totaled = False
    name = ''
    while not totaled:
        totHour = 0
        totMin = 0
        for hour in individualHours:
            if individualHours[0][0] == hour[0]:
                totalingActivity.append(hour)
        for hour in totalingActivity:
            totHour += hour[1]
            totMin += hour[2]
            name = hour[0]
        if totMin > 59:
            totHour += round(totMin / 60)
        if totHour < 1:
            totHour = totMin / 100
        # Follows the same route with listing as process(). Here, many calculations happen.

        for item in totalingActivity:
            individualHours.remove(item)
        totalingActivity.clear()
        if len(individualHours) == 0:
            totaled = True
        leaderboard.append([name, totHour])
    leaderboard = sorted(leaderboard, key=lambda x: (x[1]), reverse=True)
    WriteFile = open(f'text files/processed_{month}21.txt', 'w')
    for item in leaderboard:
        WriteFile.write(f"{item[0]} - **{item[1]}h**\n")
    # Finishes everything up and writes to a file, in a sorted form from most to least.


def total_json(month):
    leaderboard = []
    totaled = False
    name = ''
    while not totaled:
        total_hours = 0
        total_minutes = 0
        for hour in individualHours:
            if individualHours[0]['userid'] == hour['userid']:
                totalingActivity.append(hour)
        for hour in totalingActivity:
            total_hours += hour['hours']
            total_minutes += hour['minutes']
            name = hour['user']
        if total_minutes > 59:
            total_hours += round(total_minutes / 60)
        if total_hours < 1:
            total_hours = total_minutes / 100
        # Follows the same route with listing as process(). Here, many calculations happen.

        for item in totalingActivity:
            individualHours.remove(item)
        totalingActivity.clear()
        if len(individualHours) == 0:
            totaled = True
        leaderboard.append([name, total_hours])
    leaderboard = sorted(leaderboard, key=lambda x: (x[1]), reverse=True)
    WriteFile = open(f'text files/processed_{month}21.txt', 'w')
    for item in leaderboard:
        WriteFile.write(f"{item[0]} - **{item[1]}h**\n")
    # Finishes everything up and writes to a file, in a sorted form from most to least.


if __name__ != '__main__':
    opendoc('aug')
    process()
    total('aug')

if __name__ == '__main__':
    rawActivity = opendoc_json('aug')
    # Don't forget to use return and assigning when you assign a value to a variable!!!!
    process_json()
    total_json('aug')
