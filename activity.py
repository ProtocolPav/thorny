OpenFile = 'abcd'
rawActivity = []
processingActivity = []
individualHours = []
totalingActivity = []


def resetValues():
    rawActivity.clear()
    processingActivity.clear()
    individualHours.clear()
    totalingActivity.clear()


def opendoc(month):
    OpenFile = open(f'text files/activity_{month}21.txt', 'r')
    for line in OpenFile:
        field = line.split(',')
        if len(field) > 1:
            status = field[0]
            date = field[1]
            time = field[3]
            player = field[4]
            playerid = field[5]
            rawActivity.append([status, player[1:len(player)], date[1:len(date)], time[1:len(time)], playerid[1:len(playerid)]])
        else:
            field.remove(line)
    # Opens the file, adds fields into the raw list for it to begin processing


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
            if processingActivity.index(log) == len(processingActivity)-1:
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
            elif log[0] == 'CONNECT' and processingActivity[processingActivity.index(log)+1][0] == 'DISCONNECT':
                cHour = int(log[3][0:2])
                cMin = int(log[3][3:5])
                dcHour = int(processingActivity[processingActivity.index(log)+1][3][0:2])
                dcMin = int(processingActivity[processingActivity.index(log)+1][3][3:5])

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
            elif log[0] == 'CONNECT' and processingActivity[processingActivity.index(log)+1][0] == 'CONNECT':
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


def totalize(month):
    leaderboard = []
    totalized = False
    name = ''
    while not totalized:
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
            totalized = True
        leaderboard.append([name, totHour])
    leaderboard = sorted(leaderboard, key= lambda x:(x[1]), reverse=True)
    WriteFile = open(f'text files/processed_{month}21.txt', 'w')
    for item in leaderboard:
        WriteFile.write(f"{item[0]} - **{item[1]}h**\n")
    # Finishes everything up and writes to a file, in a sorted form from most to least.


if __name__ == '__main__':
    opendoc('aug')
    process()
    totalize('aug')