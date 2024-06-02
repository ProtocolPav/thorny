from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional


@dataclass
class DailyPlaytime:
    day: datetime
    playtime: timedelta

    @classmethod
    def build(cls, daily: dict):
        return cls(day=datetime.strptime(daily['day'], "%Y-%m-%d"),
                   playtime=timedelta(seconds=daily['playtime']))

@dataclass
class MonthlyPlaytime:
    month: datetime
    playtime: timedelta

    @classmethod
    def build(cls, monthly: dict):
        return cls(month=datetime.strptime(monthly['month'], "%Y-%m-%d"),
                   playtime=timedelta(seconds=monthly['playtime']))


@dataclass
class Playtime:
    total: timedelta
    session: Optional[datetime]
    daily: list[DailyPlaytime]
    monthly: list[MonthlyPlaytime]

    @classmethod
    def build(cls, playtime: dict):
        session = datetime.strptime(playtime['session'], "%Y-%m-%d %H:%M:%S.%f") if playtime['session'] else None
        return cls(total=timedelta(seconds=playtime['total']),
                   session=session,
                   daily=[DailyPlaytime.build(i) for i in playtime['daily']],
                   monthly=[MonthlyPlaytime.build(i) for i in playtime['monthly']])
