import asyncpg as pg
from datetime import datetime, timedelta
import discord
from thorny_core import errors
from dataclasses import dataclass, field
from thorny_core.db._model import Column


@dataclass
class Profile:
    column_data: pg.Record = field(repr=False)
    slogan: str = None
    gamertag: str = None
    role: str = None
    aboutme: str = None
    lore: str = None
    information_shown: bool = True
    aboutme_shown: bool = True
    activity_shown: bool = True
    lore_shown: bool = True

    def __init__(self, profile_data, column_data):
        self.column_data = column_data
        self.slogan = profile_data['slogan']
        self.gamertag = profile_data['gamertag']
        self.role = profile_data['role']
        self.aboutme = profile_data['aboutme']
        self.lore = profile_data['lore']
        self.information_shown = profile_data['information_shown']
        self.activity_shown = profile_data['activity_shown']
        self.lore_shown = profile_data['lore_shown']

        if self.slogan is None:
            self.slogan_default = "Your Slogan Goes Here"
        if self.role is None:
            self.role_default = "Wandering Dweller"
        if self.aboutme is None:
            self.aboutme_default = "I'm a pretty cool person!"
        if self.lore is None:
            self.lore_default = "I came from a distant land, far away from here..."

    def update(self, attribute, value=None, toggle=False):
        if toggle:
            attr_to_toggle = self.__getattribute__(attribute)
            self.__setattr__(attribute, not attr_to_toggle)
        else:
            for data in self.column_data:
                if data["column_name"] == str(attribute) and (data["character_maximum_length"] is None or
                                                              data["character_maximum_length"] >= len(value)):
                    self.__setattr__(attribute, value)
                    break
                elif data["column_name"] == str(attribute) and data["character_maximum_length"] < len(value):
                    raise errors.DataTooLongError(len(value), data["character_maximum_length"])


@dataclass
class Level:
    level: int
    xp: int
    required_xp: int

    def __init__(self, level_data):
        self.level = level_data['user_level']
        self.xp = level_data['xp']
        self.required_xp = level_data['required_xp']


@dataclass
class Playtime:
    total_playtime: timedelta = None
    current_playtime: timedelta = None
    previous_playtime: timedelta = None
    expiring_playtime: timedelta = None
    recent_session: timedelta = None
    daily_average: timedelta = None
    session_average: timedelta = None

    def __init__(self, playtime_data, latest_playtime, daily_average):
        self.total_playtime = playtime_data['total_playtime']
        self.current_playtime = playtime_data['current_playtime']
        self.previous_playtime = playtime_data['previous_playtime']
        self.expiring_playtime = playtime_data['expiring_playtime']
        self.recent_session = latest_playtime['playtime']
        self.daily_average = daily_average['averages']


@dataclass
class InventorySlot:

