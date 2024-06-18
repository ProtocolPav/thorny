import discord

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from thorny_core import thorny_errors

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
                                          json={'name': name,
                                                'description': description,
                                                'coordinates_x': coordinates[0],
                                                'coordinates_y': coordinates[1],
                                                'coordinates_z': coordinates[2],
                                                'owner_id': owner_id,
                                                'thread_id': None,
                                                'completed_on': None})

            if project.status_code != 200:
                raise thorny_errors.UnexpectedError2('There was an issue creating your project. '
                                                     'Most likely, the project ID is already taken.')

            return cls(**project.json()['project'], members=project.json()['members'],
                       status=project.json()['status']['status'], status_since=project.json()['status']['status_since'])

    @classmethod
    async def build(cls, project_id: str):
        async with httpx.AsyncClient() as client:
            project = await client.get(f"http://nexuscore:8000/api/v0.1/projects/{project_id}")

            return cls(**project.json()['project'], members=project.json()['members'],
                       status=project.json()['status']['status'], status_since=project.json()['status']['status_since'])

    async def update(self):
        async with httpx.AsyncClient() as client:
            data = {
                     'name': self.name,
                     'description': self.description,
                     'coordinates_x': self.coordinates_x,
                     'coordinates_y': self.coordinates_y,
                     'coordinates_z': self.coordinates_z,
                     'owner_id': self.owner_id,
                     'thread_id': self.thread_id,
                     'completed_on': self.completed_on
                    }

            project = await client.patch(f"http://nexuscore:8000/api/v0.1/projects/{self.project_id}",
                                         json=data)

            if project.status_code != 200:
                raise thorny_errors.UserUpdateError

    async def set_status(self, status: str):
        async with httpx.AsyncClient() as client:
            data = {
                     'status': status
                    }

            project = await client.post(f"http://nexuscore:8000/api/v0.1/projects/{self.project_id}/status",
                                        json=data)

            if project.status_code != 201:
                raise thorny_errors.UserUpdateError

            self.status = status
            self.status_since = datetime.now()
