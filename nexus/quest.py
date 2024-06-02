import discord

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional


@dataclass
class Reward:
    reward_id: int
    quest_id: int
    objective_id: Optional[int]
    balance: Optional[int]
    item: Optional[str]
    count: Optional[int]


@dataclass
class Objective:
    objective_id: int
    quest_id: int
    objective: str
    order: int
    objective_count: int
    objective_type: str
    objective_timer: Optional[timedelta]
    required_mainhand: Optional[str]
    required_location: Optional[list]
    location_radius: int


@dataclass
class Quest:
    quest_id: int
    start_time: datetime
    end_time: datetime
    timer: timedelta
    title: str
    description: str
    rewards: list[Reward]
    objectives: list[Objective]


@dataclass
class UserObjective:
    quest_id: int
    objective_id: int
    start: datetime
    end: datetime
    completion: int
    status: str


@dataclass
class UserQuest:
    quest_id: int
    accepted_on: datetime
    started_on: datetime
    objectives_completed: int
    status: str
    objectives: list[UserObjective]