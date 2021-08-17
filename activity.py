def matching(item1, item2):
    if int(item2) == int(item1) or int(item2) - int(item1) == 1:
        return True
    else:
        return False


def compare():
    comparelist.clear()
    connectfound = False
    discfound = False
    # Checks for CONNECT and DISCONNECT keywords, once one is found, a flag is turned to TRUE.
    # If there is no C/DC Pair, it takes the single C and logs it as 2h
    for log in activitylist:
        if log[0] == 'CONNECT' and len(comparelist) == 0 and not connectfound:
            comparelist.append(log)
            connectfound = True
        elif log[0] == 'DISCONNECT' and len(comparelist) == 0:
            pass
        elif log[0] == 'DISCONNECT' and log[3] == comparelist[0][3] and not discfound:
            if matching(comparelist[0][1][5:7], log[1][5:7]):
                comparelist.append(log)
                discfound = True
            else:
                connectfound = False
                comparelist.clear()
        else:
            pass
    # Here is where all the time calculations happen
    print(comparelist)
    if len(comparelist) == 2 and matching(comparelist[0][1][5:7], comparelist[1][1][5:7]):
        time1 = int(comparelist[0][2][0:2])
        time2 = int(comparelist[1][2][0:2])

        mtime1 = int(comparelist[0][2][3:5])
        mtime2 = int(comparelist[1][2][3:5])

        hrsplayed = time2 - time1
        minsplayed = mtime2 - mtime1
        if hrsplayed < 0:
            hrsplayed += 24
        if hrsplayed >= 12:
            hrsplayed = 2
        if minsplayed < 0:
            minsplayed += 60
        activitylist.remove(comparelist[0])
        activitylist.remove(comparelist[1])
    else:
        hrsplayed = 2
        minsplayed = 0
        activitylist.remove(comparelist[0])
    # Player, time is written onto a file
    #WriteFile = open(f'processed_{month}21.txt', 'a')
    #WriteFile.write(f"{comparelist[0][3]} - {hrsplayed}h{minsplayed}m\n")
    playlist.append([comparelist[0][3], hrsplayed, minsplayed])
    print(f"{comparelist[0][3]} - {hrsplayed}h{minsplayed}m")


def processlist():
    connect = 0
    disconnect = 0
    comparelist.clear()

    for log in activitylist:
        while len(comparelist) < 3:
            if log[0] == 'CONNECT':
                if len(comparelist) == 0 and connect == 0:
                    comparelist.append(log)
                    connect = 1
                    print(f"C1 {log}")
                elif len(comparelist) == 1 and connect == 1 and log[1] == comparelist[0][1]:
                    comparelist.append(log)
                    connect = 2
                    print(f"DUBC {log}")
                else:
                    pass
            if log[0] == 'DISCONNECT':
                if connect == 2:
                    comparelist.append(log)
                    disconnect = 1
                    print(f"DC {log}")
                elif len(comparelist) == 1 and connect == 1:
                    if log[1] == comparelist[0][1]:
                        comparelist.append(log)
                        disconnect = 1
                        print(f"DC {log}")
                    else:
                        pass
                elif len(comparelist) == 0 and connect == 0:
                    pass
                else:
                    pass
        print(f'LIST FULL\n{comparelist}')
        if comparelist[0][0] == 'CONNECT':
            if matching(comparelist[0][2][5:7], comparelist[1][2][5:7]):
                time1 = int(comparelist[0][3][0:2])
                time2 = int(comparelist[1][3][0:2])

                mtime1 = int(comparelist[0][3][3:5])
                mtime2 = int(comparelist[1][3][3:5])

                hrsplayed = time2 - time1
                minsplayed = mtime2 - mtime1
                if hrsplayed < 0:
                    hrsplayed += 24
                if hrsplayed >= 12:
                    hrsplayed = 2
                if minsplayed < 0:
                    minsplayed += 60
            else:
                hrsplayed = 2
                minsplayed = 0
        else:
            comparelist.clear()
        playlist.append([comparelist[0][3], hrsplayed, minsplayed])
        print(f"{comparelist[0][3]} - {hrsplayed}h{minsplayed}m")
        for item in comparelist:
            activitylist.remove(item)


def total():
    name = playlist[0][0]
    print(playlist)
    totalh = 0
    totalm = 0
    index = 0
    for session in playlist:
        if session[0] == name:
            comparelist.append(session)
            index += 1
            print('Name got', session[0], index)
        else:
            pass
            print('passed')
    del playlist[0:index]

    for item in comparelist:
        totalh += item[1]
        totalm += item[2]
    if totalm > 59:
        totalh += round(totalm / 60)
    if totalh < 1:
        totalh = totalm/100
    print(f"{name} - {totalh}h")
    WriteFile = open(f'processed_{month}21.txt', 'a')
    WriteFile.write(f"{name} - {totalh}h\n")
    comparelist.clear()

timeplayed = 0
comparelist = []
activitylist = []
playlist = []

month = input('Select month to log: ').lower()[0:3]
ActiveFile = open(f'activity_{month}21.txt', 'r')
for line in ActiveFile:
    field = line.split(',')
    if len(field) > 1:
        status = field[0]
        date = field[1]
        time = field[3]
        player = field[4]
        playerid = field[5]
        activitylist.append([status, date[1:len(date)], time[1:len(time)], player[1:len(player)]])
        #activitylist.append([status, player[1:len(player)], date[1:len(date)], time[1:len(time)]])
    else:
        field.remove(line)

while len(activitylist) > 1:
    print(len(activitylist))
    print(activitylist)
    compare()
playlist = sorted(playlist)
while len(playlist) > 0:
    print(len(playlist))
    total()
print('ACTIVITY LOGGED')
