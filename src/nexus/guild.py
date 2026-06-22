import discord

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Literal

from nexuscore_client import AuthenticatedClient
from nexuscore_client.api.guilds import (
    get_guild_v1_guilds_me_get,
    partial_update_guild_v1_guilds_me_patch,
    create_guild_v1_guilds_post,
    get_online_members_v1_guilds_me_online_get
)
from nexuscore_client.api.leaderboards import (
    get_playtime_leaderboard_v1_guilds_me_leaderboard_playtime_month_get,
    get_quests_leaderboard_v1_guilds_me_leaderboard_quests_router_get,
    get_currency_leaderboard_v1_guilds_me_leaderboard_currency_get,
    get_levels_leaderboard_v1_guilds_me_leaderboard_levels_get
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
        data = GuildIn(guild_id=guild.id, name=guild.name)

        guild_object = await create_guild_v1_guilds_post.asyncio_detailed(client=api, body=data)

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

            guild_dict['features'] = [Feature(**f.to_dict()) for f in guild_object.parsed.features]
            guild_dict['channels'] = [Channel(**c.to_dict()) for c in guild_object.parsed.channels]

            guild_class = cls(**guild_dict, discord_guild=guild)

            guild_class.name = guild.name
            guild_class.active = True

            await guild_class.update(api)

            return guild_class

    async def update(self, api: AuthenticatedClient):
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

        guild = await partial_update_guild_v1_guilds_me_patch.asyncio_detailed(client=api, body=data)

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

    @staticmethod
    async def get_playtime_leaderboard(api: AuthenticatedClient, month: date) -> list[dict]:
        async with api as client:
            lb = await get_playtime_leaderboard_v1_guilds_me_leaderboard_playtime_month_get.asyncio(client=client, month=month)

            return lb.to_dict()['leaderboard']

    @staticmethod
    async def get_money_leaderboard(api: AuthenticatedClient) -> list[dict]:
        async with api as client:
            lb = await get_currency_leaderboard_v1_guilds_me_leaderboard_currency_get.asyncio(client=client)

            return lb.to_dict()['leaderboard']

    @staticmethod
    async def get_levels_leaderboard(api: AuthenticatedClient) -> list[dict]:
        async with api as client:
            lb = await get_levels_leaderboard_v1_guilds_me_leaderboard_levels_get.asyncio(client=client)

            return lb.to_dict()['leaderboard']

    @staticmethod
    async def get_quests_leaderboard(api: AuthenticatedClient) -> list[dict]:
        async with api as client:
            lb = await get_quests_leaderboard_v1_guilds_me_leaderboard_quests_router_get.asyncio(client=client)

            return lb.to_dict()['leaderboard']

    @staticmethod
    async def get_online_players(api: AuthenticatedClient) -> list[OnlineUser]:
        async with api as client:
            lb = await get_online_members_v1_guilds_me_online_get.asyncio(client=client)

            online_users = []
            for user in lb:
                user = user.to_dict()
                user['session'] = datetime.fromisoformat(user['session'])

                online_users.append(OnlineUser(**user))

            return online_users