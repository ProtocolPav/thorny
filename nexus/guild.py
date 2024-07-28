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
    async def build(cls, guild_id: int) -> list["Feature"]:
        async with httpx.AsyncClient() as client:
            features_response = await client.get(f"http://nexuscore:8000/api/v0.1/guilds/{guild_id}/features")
            features = features_response.json()

            return_list = []
            for i in features['features']:
                return_list.append(cls(**i))

            return return_list


@dataclass
class Channel:
    channel_type: str
    channel_id: int

    @classmethod
    async def build(cls, guild_id: int) -> list["Channel"]:
        async with httpx.AsyncClient() as client:
            channels_response = await client.get(f"http://nexuscore:8000/api/v0.1/guilds/{guild_id}/channels")
            channels = channels_response.json()

            return_list = []
            for i in channels['channels']:
                return_list.append(cls(**i))

            return return_list


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
            data = {'guild_id': guild.id, 'name': guild.name}

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

            features = await Feature.build(guild.id)
            channels = await Channel.build(guild.id)

            guild_class = cls(**guild_dict, discord_guild=guild, features=features, channels=channels)

            guild_class.name = guild.name
            guild_class.active = True

            await guild_class.update()

            return guild_class

    async def update(self):
        async with httpx.AsyncClient() as client:
            data = {
                      "name": self.name,
                      "currency_name": self.currency_name,
                      "currency_emoji": self.currency_emoji,
                      "level_up_message": self.level_up_message,
                      "join_message": self.join_message,
                      "leave_message": self.leave_message,
                      "xp_multiplier": self.xp_multiplier,
                      "active": self.active
                    }

            guild = await client.patch(f"http://nexuscore:8000/api/v0.1/guilds/{self.guild_id}",
                                       json=data)

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
            lb = await client.get(f"http://nexuscore:8000/api/v0.1/guilds/{self.guild_id}/leaderboard/playtime/{month}",
                                  timeout=None)

            return lb.json()['leaderboard']

    async def get_money_leaderboard(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            lb = await client.get(f"http://nexuscore:8000/api/v0.1/guilds/{self.guild_id}/leaderboard/currency",
                                  timeout=None)

            return lb.json()['leaderboard']


    async def get_levels_leaderboard(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            lb = await client.get(f"http://nexuscore:8000/api/v0.1/guilds/{self.guild_id}/leaderboard/levels",
                                  timeout=None)

            return lb.json()['leaderboard']


    async def get_quests_leaderboard(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            lb = await client.get(f"http://nexuscore:8000/api/v0.1/guilds/{self.guild_id}/leaderboard/quests",
                                  timeout=None)

            return lb.json()['leaderboard']

    async def get_online_players(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            lb = await client.get(f"http://nexuscore:8000/api/v0.1/guilds/{self.guild_id}/online",
                                  timeout=None)

            return lb.json()['users']