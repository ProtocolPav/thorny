import discord

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional

import httpx


@dataclass
class Project:
    project_id: str
    name: str
    description: str
    coordinates_x: int
    coordinates_y: int
    coordinates_z: int
    thread_id: int
    started_on: date
    completed_on: date
    owner_id: int
    members: list[int]
    status: str
    status_since: datetime

    @classmethod
    async def create_new_project(cls, name: str, description: str, coordinates: list[int], owner_id: int):
        async with httpx.AsyncClient() as client:
            project = await client.post(f"http://nexuscore:8000/api/v0.1/projects",
                                          json={'name': name, 'description': description,
                                                'coordinates_x': coordinates[0], 'coordinates_y': coordinates[1],
                                                'coordinates_z': coordinates[2], 'owner_id': owner_id,
                                                'thread_id': None, 'completed_on': None})

            return cls(**project.json()['project'], members=project.json()['members'],
                       status=project.json()['status']['status'], status_since=project.json()['status']['status_since'])

    @classmethod
    async def build(cls, project_id: str):
        async with httpx.AsyncClient() as client:
            project = await client.get(f"http://nexuscore:8000/api/v0.1/projects/{project_id}")

            return cls(**project.json()['project'], members=project.json()['members'],
                       status=project.json()['status']['status'], status_since=project.json()['status']['status_since'])
