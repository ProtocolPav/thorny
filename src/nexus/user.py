import random

import discord

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Optional

import httpx
from nexuscore_client import AuthenticatedClient
from nexuscore_client.api.users import (
    get_user_v1_guilds_me_users_thorny_id_get, lookup_user_v1_guilds_me_users_lookup_get,
    partial_update_user_v1_guilds_me_users_thorny_id_patch,
    create_user_v1_guilds_me_users_post
)
from nexuscore_client.models import UserIn, UserUpdate

from src import thorny_errors

from src.nexus.playtime import Playtime
from src.nexus.profile import Profile
from src.nexus.quest_progress import QuestProgress
from src.nexus.interactions import Interactions


@dataclass
class ThornyUser:
    discord_member: discord.Member
    thorny_id: int
    user_id: int
    guild_id: int
    username: str
    join_date: datetime
    birthday: Optional[datetime]
    balance: int
    active: bool
    role: str
    patron: bool
    level: int
    xp: int
    required_xp: int
    last_message: datetime
    gamertag: str
    whitelist: str
    location: Optional[tuple[int, int, int]]
    dimension: Optional[str]
    hidden: bool
    xuid: Optional[str]
    profile: Profile
    playtime: Playtime = Playtime
    quest: QuestProgress = QuestProgress
    interactions: Interactions = Interactions


    @staticmethod
    def __get_roles(member: discord.Member) -> tuple[str, bool]:
        accepted_roles = ['owner', 'community manager', 'new recruit',
                          'knight', 'builder', 'merchant', 'gatherer', 'stoner', 'bard', 'miner']

        user_roles = [role.name.lower() for role in member.roles]

        role = 'dweller'
        patron = False

        for i in accepted_roles:
            if i in user_roles:
                role = i
                break

        if 'everthorn supporter' in user_roles:
            patron = True

        return role.title(), patron

    @classmethod
    async def __create_new_user(cls, api: AuthenticatedClient, member: discord.Member):
        user_id = member.id
        guild_id = member.guild.id

        data = {'guild_id': guild_id, 'user_id': user_id, 'username': member.name}

        user = await create_user_v1_guilds_me_users_post.asyncio_detailed(client=api, body=UserIn(**data))

        if user.status_code == 201:
            return user
        else:
            raise thorny_errors.UserAlreadyExists

    @classmethod
    async def build(cls, api: AuthenticatedClient, member: discord.Member):
        """
        Builds the ThornyUser object from the NexusCore API.

        It also:
        - Creates the user if necessary
        - Updates username, role, patron and active fields
        :param member:
        :param api:
        :return:
        """
        user_id = member.id

        user_response = await lookup_user_v1_guilds_me_users_lookup_get.asyncio_detailed(client=api, discord_id=user_id)

        if user_response.status_code == 404 or user_response.status_code == 400:
            user_response = await cls.__create_new_user(api, member)

        user: dict = user_response.parsed.to_dict()

        profile = Profile(**user.pop('profile'), thorny_id=user['thorny_id'])

        user_class = cls(**user, profile=profile, discord_member=member,)

        user_class.username = member.name
        user_class.active = True
        user_class.role, user_class.patron = cls.__get_roles(member)

        user_class.last_message = datetime.fromisoformat(user['last_message'])
        user_class.join_date = datetime.fromisoformat(user['join_date'])

        if user_class.birthday:
            user_class.birthday = datetime.fromisoformat(user['birthday'])

        await user_class.update(api)

        return user_class

    @classmethod
    async def get_discord_id(cls, api: AuthenticatedClient, thorny_id: int):
        async with api as client:
            user_response = await get_user_v1_guilds_me_users_thorny_id_get.asyncio_detailed(thorny_id, client=client)

            return user_response.parsed.user_id

    async def update(self, api: AuthenticatedClient):
        data = UserUpdate(
            username=self.username,
            birthday=self.birthday,
            balance=self.balance,
            active=self.active,
            role=self.role,
            patron=self.patron,
            level=self.level,
            xp=self.xp,
            required_xp=self.required_xp,
            last_message=self.last_message,
            gamertag=self.gamertag,
            whitelist=self.whitelist,
            location=self.location,
            dimension=self.dimension,
            hidden=self.hidden
        )

        user = await partial_update_user_v1_guilds_me_users_thorny_id_patch.asyncio_detailed(self.thorny_id, client=api, body=data)

        if user.status_code != 200:
            raise thorny_errors.UserUpdateError

    async def level_up(self, api: AuthenticatedClient, xp_multiplier: float) -> bool:
        level_up = False
        time = datetime.now(UTC)

        if time - self.last_message > timedelta(minutes=1):
            self.xp += round(random.uniform(5.0*xp_multiplier, 16*xp_multiplier))
            self.last_message = time

            while self.xp > self.required_xp:
                self.level += 1
                self.required_xp += (self.level ** 2) * 4 + (50 * self.level) + 100

                level_up = True

            await self.update(api)

        return level_up
