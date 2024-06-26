from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional

@dataclass
class Playtime:
    total: timedelta
    session: Optional[datetime]
    today: timedelta
    current_month: timedelta
    second_month: timedelta
    third_month: timedelta

    @classmethod
    def build(cls, playtime: dict):
        session = datetime.strptime(playtime['session'], "%Y-%m-%d %H:%M:%S.%f") if playtime['session'] else None

        try:
            if playtime['daily'][0]['day'] == str(date.today()):
                today = playtime['daily'][0]['playtime']
            else:
                today = 0
        except IndexError:
            today = 0

        current_month = 0
        second_month = 0
        third_month = 0

        for i in range(0, len(playtime['monthly']) - 1):
            if playtime['monthly'][i]['month'] == str(date.today().replace(day=1)):
                current_month = playtime['monthly'][i]['playtime']
            elif playtime['monthly'][i]['month'] == str(date.today().replace(day=1, month=date.today().month-1)):
                second_month = playtime['monthly'][i]['playtime']
            elif playtime['monthly'][i]['month'] == str(date.today().replace(day=1, month=date.today().month-2)):
                third_month = playtime['monthly'][i]['playtime']

        return cls(total=timedelta(seconds=playtime['total']),
                   session=session,
                   today=timedelta(seconds=today),
                   current_month=timedelta(seconds=current_month),
                   second_month=timedelta(seconds=second_month),
                   third_month=timedelta(seconds=third_month))
