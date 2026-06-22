import discord

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Literal

import httpx

from nexuscore_client import AuthenticatedClient
from nexuscore_client.api.guilds import (
    get_guild_v1_guilds_me_get,
    partial_update_guild_v1_guilds_me_patch,
    create_guild_v1_guilds_post
)
from nexuscore_client.models import GuildIn, GuildUpdate

from src import thorny_errors


@dataclass
class Feature:
    feature: str
    configured: bool


@dataclass
class Channel:
    channel_type: str
    channel_id: int


@dataclass
class OnlineUser:
    thorny_id: int
    user_id: int
    session: datetime
    username: str
    whitelist: str
    location: tuple[int, int, int]
    dimension: str
    hidden: bool
    xuid: Optional[str]


@dataclass
class ThornyGuild:
    discord_guild: discord.Guild
    guild_id: int
    name: str
    currency_name: str
    currency_emoji: str
    level_up_message: str
    join_message: str
    leave_message: str
    xp_multiplier: float
    active: bool
    features: list[Feature]
    channels: list[Channel]

    @classmethod
    async def __create_new_guild(cls, api: AuthenticatedClient, guild: discord.Guild):
        async with api as client:
            data = GuildIn(guild_id=guild.id, name=guild.name)

            guild_object = await create_guild_v1_guilds_post.asyncio_detailed(client=client, body=data)

            if guild_object.status_code == 201:
                return guild_object
            else:
                raise thorny_errors.GuildAlreadyExists


    @classmethod
    async def build(cls, api: AuthenticatedClient, guild: discord.Guild):
        """
        Builds the ThornyGuild object from the NexusCore API.

        It also:
        - Creates the guild if necessary
        - Updates name and active fields (Not yet implemented by the API)
        :param guild:
        :param api:
        :return:
        """
        async with api as client:
            guild_object = await get_guild_v1_guilds_me_get.asyncio_detailed(client=client)

            if guild_object.status_code == 404:
                guild_object = await cls.__create_new_guild(api, guild)

            guild_dict = guild_object.parsed.to_dict()

            guild_class = cls(**guild_dict, discord_guild=guild)

            guild_class.name = guild.name
            guild_class.active = True

            await guild_class.update(api)

            return guild_class

    async def update(self, api: AuthenticatedClient):
        async with api as client:
            data = GuildUpdate(
                name=self.name,
                active=self.active,
                currency_name=self.currency_name,
                currency_emoji=self.currency_emoji,
                level_up_message=self.level_up_message,
                join_message=self.join_message,
                leave_message=self.leave_message,
                xp_multiplier=self.xp_multiplier
            )

            guild = await partial_update_guild_v1_guilds_me_patch.asyncio_detailed(client=client, body=data)

            if guild.status_code != 200:
                raise thorny_errors.GuildUpdateError

    def has_feature(self, feature: Literal["levels", "playtime", "basic", "beta", "everthorn", "roa"]) -> bool:
        for i in self.features:
            if i.feature == feature:
                return True

        return False

    def get_channel_id(self, channel_type: str) -> Optional[int]:
        for i in self.channels:
            if i.channel_type == channel_type:
                return i.channel_id

        return None

    async def get_playtime_leaderboard(self, month: date) -> list[dict]:
        async with httpx.AsyncClient() as client:
            lb = await client.get(f"http://nexuscore:8000/api/v0.2/guilds/{self.guild_id}/leaderboard/playtime/{month}",
                                  timeout=None)

            return lb.json()['leaderboard']

    async def get_money_leaderboard(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            lb = await client.get(f"http://nexuscore:8000/api/v0.2/guilds/{self.guild_id}/leaderboard/currency",
                                  timeout=None)

            return lb.json()['leaderboard']


    async def get_levels_leaderboard(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            lb = await client.get(f"http://nexuscore:8000/api/v0.2/guilds/{self.guild_id}/leaderboard/levels",
                                  timeout=None)

            return lb.json()['leaderboard']


    async def get_quests_leaderboard(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            lb = await client.get(f"http://nexuscore:8000/api/v0.2/guilds/{self.guild_id}/leaderboard/quests",
                                  timeout=None)

            return lb.json()['leaderboard']

    async def get_online_players(self) -> list[OnlineUser]:
        async with httpx.AsyncClient() as client:
            lb = await client.get(f"http://nexuscore:8000/api/v0.2/guilds/{self.guild_id}/online",
                                  timeout=None)

            online_users = []
            for user in lb.json():
                user['session'] = datetime.fromisoformat(user['session'])

                online_users.append(OnlineUser(**user))

            return online_users