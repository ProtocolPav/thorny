import discord

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Literal

import httpx

import thorny_core.thorny_errors as thorny_errors


@dataclass
class Feature:
    feature: str
    configured: bool

    @classmethod
    def build(cls, feature: dict):
        return cls(**feature)


@dataclass
class Channel:
    channel_type: str
    channel_id: int

    @classmethod
    def build(cls, channel: dict):
        return cls(**channel)


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
    async def __create_new_guild(cls, guild: discord.Guild):
        async with httpx.AsyncClient() as client:
            data = {'guild_id': guild.id, 'guild_name': guild.name}

            guild_object = await client.post("http://nexuscore:8000/api/v0.1/guilds/",
                                             json=data)

            if guild_object.status_code == 201:
                return guild_object
            else:
                raise thorny_errors.GuildAlreadyExists


    @classmethod
    async def build(cls, guild: discord.Guild):
        """
        Builds the ThornyGuild object from the NexusCore API.

        It also:
        - Creates the guild if necessary
        - Updates name and active fields (Not yet implemented by the API)
        :param guild:
        :return:
        """
        async with httpx.AsyncClient() as client:
            try:
                guild_object = await cls.__create_new_guild(guild)
            except thorny_errors.GuildAlreadyExists:
                guild_object = await client.get(f"http://nexuscore:8000/api/v0.1/guilds/{guild.id}")

            guild_dict = guild_object.json()

            features = [Feature.build(i) for i in guild_dict['features']]
            channels = [Channel.build(i) for i in guild_dict['channels']]

            guild_class = cls(**guild_dict['guild'], discord_guild=guild, features=features, channels=channels)

            guild_class.name = guild.name
            guild_class.active = True

            # await guild_class.update()

            return guild_class

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
            lb = await client.get(f"http://nexuscore:8000/api/v0.1/guilds/{self.guild_id}/leaderboard/playtime/{month}",
                                  timeout=None)

            return lb.json()['leaderboard']