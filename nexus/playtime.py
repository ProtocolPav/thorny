from dataclasses import dataclass
from datetime import date, datetime, timedelta
from dateutil import relativedelta
from typing import Optional

import httpx


@dataclass
class Playtime:
    total: timedelta
    session: Optional[datetime]
    today: timedelta
    current_month: timedelta
    second_month: timedelta
    third_month: timedelta

    @classmethod
    async def build(cls, thorny_id: int):
        async with httpx.AsyncClient() as client:
            playtime_response = await client.get(f"http://nexuscore:8000/api/v0.2/users/{thorny_id}/playtime",
                                                 timeout=None)

            if playtime_response.status_code != 200:
                return cls(total=timedelta(seconds=0),
                           session=None,
                           today=timedelta(seconds=0),
                           current_month=timedelta(seconds=0),
                           second_month=timedelta(seconds=0),
                           third_month=timedelta(seconds=0))

            playtime = playtime_response.json()

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
                elif playtime['monthly'][i]['month'] == str(date.today().replace(day=1, month=(date.today() - relativedelta.relativedelta(months=1)).month)):
                    second_month = playtime['monthly'][i]['playtime']
                elif playtime['monthly'][i]['month'] == str(date.today().replace(day=1, month=(date.today() - relativedelta.relativedelta(months=2)).month)):
                    third_month = playtime['monthly'][i]['playtime']

            return cls(total=timedelta(seconds=playtime['total']),
                       session=session,
                       today=timedelta(seconds=today),
                       current_month=timedelta(seconds=current_month),
                       second_month=timedelta(seconds=second_month),
                       third_month=timedelta(seconds=third_month))
