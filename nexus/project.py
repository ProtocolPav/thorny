import discord

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import thorny_errors

import httpx

from nexus import ThornyUser


@dataclass
class Project:
    project_id: str
    name: str
    description: str
    coordinates: tuple[int, int, int]
    thread_id: int
    started_on: date
    completed_on: date
    owner_id: int
    owner: ThornyUser
    members: list[int]
    status: str
    status_since: datetime

    @classmethod
    async def create_new_project(cls, name: str, description: str, coordinates: list[int], owner_id: int):
        async with httpx.AsyncClient() as client:
            project = await client.post(f"http://nexuscore:8000/api/v0.2/projects",
                                          json={'name': name,
                                                'description': description,
                                                'coordinates': coordinates,
                                                'owner_id': owner_id})

            if project.status_code != 201:
                raise thorny_errors.UnexpectedError2('There was an issue creating your project. '
                                                     'Most likely, the project ID is already taken.')

            project_json: dict = project.json()
            members = await client.get(f"http://nexuscore:8000/api/v0.2/projects/{project.json()['project_id']}/members")

            project_json.pop('owner')

            return cls(**project_json, members=[x['user_id'] for x in members.json()])

    @classmethod
    async def build(cls, project_id: str):
        async with httpx.AsyncClient() as client:
            project = await client.get(f"http://nexuscore:8000/api/v0.2/projects/{project_id}")

            if project.status_code != 200:
                raise thorny_errors.UnexpectedError2('There was an issue fetching your project. '
                                                     'Most likely, the project ID does not exist')

            project_json = project.json()
            members = await client.get(f"http://nexuscore:8000/api/v0.2/projects/{project.json()['project_id']}/members")

            project_json.pop('owner')

            return cls(**project_json, members=[x['user_id'] for x in members.json()])

    @classmethod
    async def get_all_projects_for_options(cls):
        async with httpx.AsyncClient() as client:
            projects = await client.get(f"http://nexuscore:8000/api/v0.2/projects")

            if projects.status_code == 200:
                options = [{'id': x['project_id'], 'name': x['name']} for x in projects.json()]

                return options

            return None

    async def update(self):
        async with httpx.AsyncClient() as client:
            data = {
                     'name': self.name,
                     'description': self.description,
                     'coordinates': self.coordinates,
                     'owner_id': self.owner_id,
                     'thread_id': self.thread_id,
                     'started_on': str(self.started_on),
                     'completed_on': str(self.completed_on) if self.completed_on else None
                    }

            project = await client.patch(f"http://nexuscore:8000/api/v0.2/projects/{self.project_id}",
                                         json=data)

            if project.status_code != 200:
                raise thorny_errors.UserUpdateError

    async def set_status(self, status: str):
        async with httpx.AsyncClient() as client:
            data = {
                     'status': status
                    }

            project = await client.post(f"http://nexuscore:8000/api/v0.2/projects/{self.project_id}/status",
                                        json=data)

            if project.status_code != 201:
                raise thorny_errors.UserUpdateError

            self.status = status
            self.status_since = datetime.now()
