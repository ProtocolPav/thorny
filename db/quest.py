from dataclasses import dataclass
from datetime import datetime, timedelta

import asyncpg as pg
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
        objective = self.objective.split(':')[1].capitalize().replace('_', ' ')
        extra_requirements = []
        notes = []

        if self.mainhand:
            mainhand = self.mainhand.split(':')[1].capitalize().replace('_', ' ')
            extra_requirements.append(f'using **{mainhand}**')
        if self.location:
            extra_requirements.append(f'around the coordinates **{int(self.location[0])}, {int(self.location[1])}**')
            notes.append(f'\n*Note: The quest area is a circle with radius {self.location_radius} around the coordinates given*')
        if self.timer:
            hours, remainder = divmod(self.timer.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            extra_requirements.append(f'with a time limit of **{hours}h{minutes}m**')
            notes.append(f'\n*Note: The time limit only begins when you {self.objective_type.lower()} 1 {objective}*')

        return (f'{self.objective_type.capitalize()} {self.objective_count} **{objective}(s)** {" ".join(extra_requirements)}'
                f'\n{"".join(notes)}')

    def get_rewards(self, money_symbol: str):
        if self.nugs_reward:
            return f"{self.nugs_reward} {money_symbol}"
        elif self.item_reward:
            item = self.item_reward.split(':')[1].capitalize().replace('_', ' ')
            return f"{self.item_reward_count} {item}(s)"
        else:
            return "There are no rewards available for this quest."


@dataclass
class PlayerQuest(Quest):
    completion_count: int
    accepted_on: datetime
    started_on: datetime

    def __init__(self, record: pg.Record):
        super().__init__(record)
        self.completion_count = record['completion_count']
        self.started_on = record['started_on']
        self.accepted_on = record['accepted_on']

    def quest_fail_check(self) -> bool:
        if self.timer:
            if self.started_on is not None:
                if datetime.now() - self.started_on >= self.timer:
                    return False

        return True