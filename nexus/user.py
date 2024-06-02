import discord

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

import httpx

import thorny_core.errors as thorny_errors

from thorny_core.nexus.playtime import Playtime
from thorny_core.nexus.profile import Profile
from thorny_core.nexus.quest import UserQuest


@dataclass
class ThornyUser:
    discord_member: discord.Member
    thorny_id: int
    user_id: int
    guild_id: int
    username: str
    join_date: date
    birthday: Optional[date]
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
    profile: Profile
    playtime: Playtime
    quest: Optional[UserQuest]


    @staticmethod
    def __get_roles(member: discord.Member) -> tuple[str, bool]:
        accepted_roles = ['owner', 'community manager', 'new recruit',
                          'knight', 'builder', 'merchant', 'gatherer', 'stoner', 'bard', 'excavator']

        user_roles = [role.name.lower() for role in member.roles]

        role = 'dweller'
        patron = False

        for i in accepted_roles:
            if i in user_roles:
                role = i
                break

        if 'patreon supporter' in user_roles:
            patron = True

        return role, patron


    @classmethod
    async def __create_new_user(cls, member: discord.Member):
        async with httpx.AsyncClient() as client:
            user_id = member.id
            guild_id = member.guild.id

            data = {'guild_id': guild_id, 'discord_user_id': user_id, 'username': member.name}

            user = await client.post("http://nexuscore:8000/api/v0.1/users/",
                                     json=data)

            if user.status_code == 201:
                return user
            else:
                raise thorny_errors.UserAlreadyExists


    @classmethod
    async def build(cls, member: discord.Member):
        """
        Builds the ThornyUser object from the NexusCore API.

        It also:
        - Creates the user if necessary
        - Updates username, role, patron and active fields
        :param member:
        :return:
        """
        async with httpx.AsyncClient() as client:
            user_id = member.id
            guild_id = member.guild.id

            try:
                user = await cls.__create_new_user(member)
            except thorny_errors.UserAlreadyExists:
                user = await client.get(f"http://nexuscore:8000/api/v0.1/users/guild/{guild_id}/{user_id}")

            user_dict = user.json()

            profile = Profile.build(user_dict['profile'], user_dict['user']['thorny_id'])
            playtime = Playtime.build(user_dict['playtime'])

            user_class = cls(**user_dict['user'], profile=profile, playtime=playtime, discord_member=member, quest=None)

            user_class.username = member.name
            user_class.active = True
            user_class.role, user_class.patron = cls.__get_roles(member)

            await user_class.update()

            return user_class


    async def update(self):
        async with httpx.AsyncClient() as client:
            data = {
                      "username": self.username,
                      "birthday": self.birthday,
                      "balance": self.balance,
                      "active": self.active,
                      "role": self.role,
                      "patron": self.patron,
                      "level": self.level,
                      "xp": self.xp,
                      "required_xp": self.required_xp,
                      "last_message": self.last_message,
                      "gamertag": self.gamertag,
                      "whitelist": self.whitelist
                    }

            user = await client.patch(f"http://nexuscore:8000/api/v0.1/users/thorny-id/{self.thorny_id}",
                                      json=data)

            if user.status_code != 200:
                raise thorny_errors.UserUpdateError
