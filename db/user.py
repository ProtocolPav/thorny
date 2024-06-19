from dataclasses import dataclass, field
from datetime import datetime, timedelta, date

import matplotlib.pyplot as plt

import asyncpg as pg
import discord

from thorny_core import thorny_errors
from thorny_core.db.guild import Guild
from thorny_core.db.poolwrapper import PoolWrapper
from thorny_core.db.quest import PlayerQuest


class Time:
    def __init__(self, time_object: datetime | timedelta | date):
        self.time = time_object

    def __str__(self):
        if type(self.time) == (date or datetime):
            datetime_object = datetime(year=self.time.year, month=self.time.month, day=self.time.day)
            return f"<t:{int(datetime_object.timestamp())}:D>"

        elif type(self.time) == timedelta:
            total_seconds = int(self.time.total_seconds())
            days, remainder = divmod(total_seconds, 24 * 60 * 60)
            hours, remainder = divmod(remainder, 60*60)
            minutes, seconds = divmod(remainder, 60)

            if days == 0:
                return f"{hours}h{minutes}m"
            elif days == 1:
                return f"{days} day, {hours}h{minutes}m"
            elif days > 1:
                return f"{days} days, {hours}h{minutes}m"

        return str(self.time)


@dataclass
class Profile:
    slogan: str = None
    aboutme: str = None
    gamertag: str = None
    whitelisted_gamertag: str = None
    character_name: str = None
    character_age: int = None
    character_race: str = None
    character_role: str = None
    character_origin: str = None
    character_beliefs: str = None
    stats_agility: int = None
    stats_valor: int = None
    stats_strength: int = None
    stats_charisma: int = None
    stats_creativity: int = None
    stats_ingenuity: int = None
    lore: str = None

    def __init__(self, profile: dict, gamertag, whitelist):
        self.slogan = profile['slogan']
        self.gamertag = gamertag
        self.whitelisted_gamertag = whitelist
        self.aboutme = profile['aboutme']
        self.character_name = profile['character_name']
        self.character_age = profile['character_age']
        self.character_race = profile['character_race']
        self.character_role = profile['character_role']
        self.character_origin = profile['character_origin']
        self.character_beliefs = profile['character_beliefs']
        self.agility = profile['agility'] if profile['agility'] <= 6 else 6
        self.valor = profile['valor'] if profile['valor'] <= 6 else 6
        self.strength = profile['strength'] if profile['strength'] <= 6 else 6
        self.charisma = profile['charisma'] if profile['charisma'] <= 6 else 6
        self.creativity = profile['creativity'] if profile['creativity'] <= 6 else 6
        self.ingenuity = profile['ingenuity'] if profile['ingenuity'] <= 6 else 6
        self.lore = profile['lore']

    def update(self, attribute, value=None):
        self.__setattr__(attribute, value)


@dataclass
class Level:
    level: int
    xp: int
    required_xp: int
    last_message: datetime

    def __init__(self, level, xp, required_xp, last_message):
        self.level = level
        self.xp = xp
        self.required_xp = required_xp
        self.last_message = last_message


@dataclass
class Playtime:
    total_playtime: Time = Time(timedelta(hours=0))
    current_playtime: Time = Time(timedelta(hours=0))
    previous_playtime: Time = Time(timedelta(hours=0))
    expiring_playtime: Time = Time(timedelta(hours=0))
    todays_playtime: Time = Time(timedelta(hours=0))

    def __init__(self, playtime: dict):
        monthly_data = playtime['monthly']

        if monthly_data:
            if len(monthly_data) >= 1:
                data_month = datetime.strptime(monthly_data[0]['month'], "%Y-%m-%d")
                if data_month.month == datetime.now().month:
                    self.current_playtime = Time(timedelta(seconds=monthly_data[0]['playtime']))

            if len(monthly_data) >= 2:
                data_month = datetime.strptime(monthly_data[1]['month'], "%Y-%m-%d")
                if data_month.month == datetime.now().month - 1:
                    self.previous_playtime = Time(timedelta(seconds=monthly_data[1]['playtime']))

            if len(monthly_data) >= 3:
                data_month = datetime.strptime(monthly_data[2]['month'], "%Y-%m-%d")
                if data_month.month == datetime.now().month - 2:
                    self.expiring_playtime = Time(timedelta(seconds=monthly_data[2]['playtime']))

        self.total_playtime = Time(timedelta(seconds=playtime['total']))

        if playtime['daily']:
            latest_day = datetime.strptime(playtime['daily'][0]['day'], "%Y-%m-%d")

            if latest_day == datetime.now():
                self.todays_playtime = Time(timedelta(seconds=playtime['daily'][0]['playtime']))


@dataclass
class User:
    discord_member: discord.Member = field(repr=False)
    thorny_id: int
    user_id: int
    guild_id: int
    guild: Guild
    username: str
    balance: int
    join_date: Time
    birthday: Time
    age: int
    gamertag: str
    whitelisted_gamertag: str
    profile: Profile
    level: Level
    playtime: Playtime
    quest: PlayerQuest = None

    def __init__(self, discord_member: discord.Member, thorny_guild: Guild, user: dict,
                 profile: dict, playtime: dict, quests: dict = None):
        self.discord_member = discord_member
        self.username = self.discord_member.name
        self.thorny_id = user['thorny_id']
        self.guild_id = user['guild_id']
        self.guild = thorny_guild
        self.user_id = user['user_id']
        self.balance = user['balance']
        self.join_date = Time(user['join_date'])
        self.birthday = Time(user['birthday'])
        self.gamertag = user['gamertag']
        self.whitelisted_gamertag = user['whitelist']
        if self.birthday.time is not None:
            today = datetime.now()
            self.age = today.year - self.birthday.time.year - ((today.month, today.day) < (self.birthday.time.month, self.birthday.time.day))
        else:
            self.age = 0
        self.profile = Profile(profile=profile, gamertag=self.gamertag, whitelist=self.whitelisted_gamertag)
        self.level = Level(level=user['level'], xp=user['xp'], required_xp=user['required_xp'],
                           last_message=user['last_message'])
        self.playtime = Playtime(playtime=playtime)
        # if current_quest is not None:
        #     self.quest = PlayerQuest(current_quest)

    async def update(self, attribute, value):
        self.__setattr__(attribute, value)
