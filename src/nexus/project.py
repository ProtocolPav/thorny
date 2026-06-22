from typing import Optional

from dataclasses import dataclass
from datetime import date, datetime

from nexuscore_client import AuthenticatedClient
from nexuscore_client.models import ProjectIn, ProjectUpdate, StatusEnum, StatusIn

from src import thorny_errors

import httpx

from nexuscore_client.api.projects import (
    list_projects_v1_guilds_me_projects_get,
    get_project_v1_guilds_me_projects_project_id_get,
    create_project_v1_guilds_me_projects_post,
    partial_update_project_v1_guilds_me_projects_project_id_patch,
    create_project_status_v1_guilds_me_projects_project_id_status_post
)


@dataclass
class Project:
    project_id: str
    name: str
    description: str
    coordinates: tuple[int, int, int]
    thread_id: int
    started_on: date
    completed_on: date
    dimension: str
    pin_id: Optional[int]
    owner_id: int
    members: list[int]
    status: str
    status_since: datetime

    @classmethod
    async def create_new_project(cls, api: AuthenticatedClient, name: str, description: str, coordinates: list[int], owner_id: int, dimension: str):
        data = {'name': name,
                'description': description,
                'coordinates': coordinates,
                'owner_id': owner_id,
                'pin_id': None,
                'dimension': dimension}
        project = await create_project_v1_guilds_me_projects_post.asyncio_detailed(client=api, body=ProjectIn(**data))

        if project.status_code != 201:
            raise thorny_errors.UnexpectedError2('There was an issue creating your project. '
                                                 'Most likely, the project ID is already taken.')

        project_json: dict = project.parsed.to_dict()
        members = []

        project_json['owner_id'] = project_json['owner']['thorny_id']
        project_json.pop('owner')

        return cls(**project_json, members=[x.user_id for x in members])

    @classmethod
    async def build(cls, api: AuthenticatedClient, project_id: str):
        project = await get_project_v1_guilds_me_projects_project_id_get.asyncio_detailed(project_id, client=api)

        if project.status_code != 200:
            raise thorny_errors.UnexpectedError2('There was an issue fetching your project. '
                                                 'Most likely, the project ID does not exist')

        project_json = project.parsed.to_dict()
        members = [] # API currently does not expose a members endpoint. Add in later.

        project_json['owner_id'] = project_json['owner']['thorny_id']
        project_json.pop('owner')

        return cls(**project_json, members=[x.user_id for x in members])

    @classmethod
    async def get_all_projects_for_options(cls, api: AuthenticatedClient):
        projects = await list_projects_v1_guilds_me_projects_get.asyncio_detailed(client=api)

        if projects.status_code == 200:
            options = [{'id': x.project_id, 'name': x.name} for x in projects.parsed]

            return options

        return None

    async def update(self, api: AuthenticatedClient):
        data = ProjectUpdate(
            name=self.name,
            description=self.description,
            coordinates=list(self.coordinates),
            owner_id=self.owner_id,
            thread_id=self.thread_id,
            completed_on=self.completed_on,
            dimension=self.dimension
        )

        project = await partial_update_project_v1_guilds_me_projects_project_id_patch.asyncio_detailed(self.project_id, body=data, client=api)

        if project.status_code != 200:
            raise thorny_errors.UserUpdateError

    async def set_status(self, api: AuthenticatedClient, status: StatusEnum):
        project = await create_project_status_v1_guilds_me_projects_project_id_status_post.asyncio_detailed(self.project_id, body=StatusIn(status=status), client=api)

        if project.status_code != 201:
            raise thorny_errors.UserUpdateError

        self.status = status
        self.status_since = datetime.now()
