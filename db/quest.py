from dataclasses import dataclass, field
from datetime import datetime, timedelta, date
from thorny_core.db.poolwrapper import PoolWrapper

import asyncpg as pg
from thorny_core.db.user import User
import discord


@dataclass
class Quest:
    id: int
    title: str
    description: str
    start: datetime
    end: datetime
    objective: str
    objective_type: str
    objective_count: int
    mainhand: str | None
    location: tuple[int, int] | None
    location_radius: int | None
    timer: timedelta | None
    nugs_reward: int | None
    item_reward: str | None
    item_reward_count: int | None

    def __init__(self, record: pg.Record):
        self.id = record['id']
        self.title = record['title']
        self.description = record['description']
        self.start = record['start_time']
        self.end = record['end_time']
        self.objective = record['objective']
        self.objective_type = record['objective_type']
        self.objective_count = record['objective_count']
        self.mainhand = record['required_mainhand']
        self.location = record['required_location']
        self.location_radius = record['location_radius']
        self.timer = record['required_timer']
        self.nugs_reward = record['balance_reward']
        self.item_reward = record['item_reward']
        self.item_reward_count = record['item_reward_count']

    def get_objective(self):
        objective = self.objective.split('minecraft:')[1].capitalize().replace('_', ' ')
        extra_requirements = []

        if self.mainhand:
            mainhand = self.mainhand.split('minecraft:')[1].capitalize().replace('_', ' ')
            extra_requirements.append(f'using **{mainhand}**')
        if self.location:
            extra_requirements.append(f'around the coordinates **{self.location[0]}x, {self.location[1]}z**')
        if self.timer:
            extra_requirements.append(f'with a time limit of {self.timer}')

        return f'{self.objective_type.capitalize()} {self.objective_count} **{objective}** {" ".join(extra_requirements)}'
