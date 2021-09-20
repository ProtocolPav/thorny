import random
import discord


def create_ticket(ctx_author, amount):
    TicketFile = open('text files/ticket.txt', 'r')
    List = []
    NumList = []
    number = 0
    for line in TicketFile:
        field = line.split(',')
        number += 1
        num = int(field[0])
        name = field[1]
        List.append(name)
        NumList.append(num)
    TicketFile.close()
    for i in range(0, amount):
        InList = True
        while InList:
            num = random.randint(3000, 3200)
            if num in NumList:
                InList = True
            else:
                InList = False
        TicketFile = open('text files/ticket.txt', 'a')
        TicketFile.write(f'{num},{ctx_author},\n')
        return num


def winners(client):
    TicketFile = open('text files/ticket.txt', 'r')
    list = []
    List = []
    NumList = []
    number = 0
    for line in TicketFile:
        field = line.split(',')
        number += 1
        num = int(field[0])
        name = field[1]
        List.append(name)
        NumList.append(num)
    TicketFile.close()
    for winner in range(1, 7):
        winnum = random.randint(1, number)
        list.append(NumList[winnum])
    return list
