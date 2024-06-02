import discord

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional


@dataclass
class DailyPlaytime:
    day: date
    playtime: timedelta

    @classmethod
    def build(cls, daily: dict):
        return cls(**daily)

@dataclass
class MonthlyPlaytime:
    month: date
    playtime: timedelta

    @classmethod
    def build(cls, monthly: dict):
        return cls(**monthly)


@dataclass
class Playtime:
    total: timedelta
    session: Optional[datetime]
    daily: list[DailyPlaytime]
    monthly: list[MonthlyPlaytime]

    @classmethod
    def build(cls, playtime: dict):
        return cls(total=playtime['total'],
                   session=playtime['session'],
                   daily=[DailyPlaytime.build(i) for i in playtime['daily']],
                   monthly=[MonthlyPlaytime.build(i) for i in playtime['monthly']])
