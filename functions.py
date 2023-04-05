import json
import os
from datetime import datetime, timedelta, date
import asyncio
import discord
import discord.ext
from dateutil import relativedelta


def calculate_reward(prize_list, prizes):
    nugs_reward = 0
    for item in prize_list:
        nugs_reward += item[1]
    if prize_list[0] != prize_list[1] != prize_list[2] != prize_list[3] and prizes[5] not in prize_list:
        nugs_reward = nugs_reward * 2
    return nugs_reward
