from dataclasses import dataclass, field
from datetime import datetime, timedelta, date
from thorny_core.db.poolwrapper import PoolWrapper

import asyncpg as pg
from thorny_core.db.user import User
import discord

@dataclass
class ProjectUpdate:
    update_id: int
    update_comment: int
    update_date: datetime


@dataclass
class ProjectRating:
    rating_id: int
    thorny_id: int
    rating_date: datetime
    rating: int
    rating_comment: str


@dataclass
class Project:
    connection_pool: PoolWrapper = field(repr=False)
    project_id: int
    owner: User
    name: str
    thread_id: int
    status: str
    coordinates: str
    description: str
    time_estimation: str
    road_built: str
    members: str
    progress: float
    ratings: list[ProjectRating]
    updates: list[ProjectUpdate]
    accept_date: datetime
    complete_date: datetime

    def __init__(self, pool_wrapper: PoolWrapper, owner: User, project_data: pg.Record):
        self.connection_pool = pool_wrapper
        self.project_id = project_data['project_id']
        self.owner = owner
        self.name = project_data['name']
        self.thread_id = project_data['thread_id']
        self.status = project_data['status']
        self.coordinates = project_data['coordinates']
        self.description = project_data['description']
        self.time_estimation = project_data['time_estimation']
        self.road_built = project_data['road_built']
        self.members = project_data['members'] if project_data['members'] is not None else ""
        self.progress = project_data['progress']
        self.accept_date = project_data['accepted_on']
        self.complete_date = project_data['completed_on']