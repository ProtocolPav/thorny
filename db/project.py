from dataclasses import dataclass, field
from datetime import datetime, timedelta, date

import asyncpg as pg
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
    project_id: int
    name: str
    thread: int
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

    def __init__(self, project_data: pg.Record):
        self.project_id = project_data['project_id']
        self.name = project_data['name']
        self.thread = project_data['thread_id']
        self.status = project_data['status']
        self.coordinates = project_data['coordinates']
        self.description = project_data['description']
        self.time_estimation = project_data['time_estimation']
        self.road_built = project_data['road_built']
        self.members = project_data['members']
        self.progress = project_data['progress']
        self.accept_date = project_data['accepted_on']
        self.complete_date = project_data['completed_on']