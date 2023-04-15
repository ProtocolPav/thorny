from dataclasses import dataclass, field
from datetime import datetime, timedelta, date

import asyncpg as pg
import discord

from thorny_core.db.poolwrapper import PoolWrapper


class Time:
    def __init__(self, time_object: datetime | timedelta | date):
        self.time = time_object

    def __str__(self):
        if type(self.time) == (date or datetime):
            datetime_string = datetime.strftime(self.time, "%B %d, %Y")
            return datetime_string
        elif type(self.time) == timedelta:
            total_seconds = int(self.time.total_seconds())
            days, remainder = divmod(total_seconds, 24 * 60 * 60)
            hours, remainder = divmod(remainder, 60*60)
            minutes, seconds = divmod(remainder, 60)

            if days == 0:
                return f"{hours}h{minutes}m"
            elif days == 1:
                return f"{days} day, {hours}h{minutes}m"
            elif days > 1:
                return f"{days} days, {hours}h{minutes}m"

        return str(self.time)


@dataclass
class Channels:
    """
    Available channels:
    - welcome
    - logs
    - gulag
    - project_forum
    - project_applications
    - thorny_updates
    """
    __channels: list

    def __init__(self, all_channels: list[pg.Record]):
        self.__channels = []
        for channel in all_channels:
            self.__channels.append({
                                    "channel_type": channel['channel_type'],
                                    "channel_id": channel['channel_id']
                                    })

    def get_channel(self, channel_type: str) -> int:
        for channel in self.__channels:
            if channel['channel_type'] == channel_type:
                return channel['channel_id']

        return 0

    def all_channels(self):
        return self.__channels


@dataclass
class Roles:
    timeout_role: int
    roles_on_join: list[int]
    admin_roles: list[int]

    def __init__(self, all_roles: dict):
        self.timeout_role = all_roles['timeout']
        self.roles_on_join = all_roles['role_on_join']
        self.admin_roles = all_roles['admin']


@dataclass
class Currency:
    name: str
    emoji: str
    total_in_circulation: int

    def __init__(self, currency_name: str, currency_emoji: str, total: int):
        self.name = currency_name
        self.emoji = currency_emoji
        self.total_in_circulation = total


@dataclass
class Reaction:
    reaction_id: int
    message_id: int
    emoji: str
    role_id: int
    role_name: int

    def __init__(self, reaction_record: pg.Record):
        self.reaction_id = reaction_record['reaction_id']
        self.message_id = reaction_record['message_id']
        self.emoji = reaction_record['emoji']
        self.role_id = reaction_record['role_id']
        self.role_name = reaction_record['role_name']


@dataclass
class Responses:
    exact: dict[str, list[str]]
    wildcard: dict[str, list[str]]

    def __init__(self, response_record: list[pg.Record]):
        self.exact = {}
        self.wildcard = {}
        for response in response_record:
            trigger = response['trigger']
            response_string = response['response']

            if response['response_type'] == 'exact':
                self.exact[trigger] = self.exact.get(trigger, list())
                self.exact[trigger].append(response_string)

            elif response['response_type'] == 'wildcard':
                self.wildcard[trigger] = self.wildcard.get(trigger, list())
                self.wildcard[trigger].append(response_string)


@dataclass
class Activity:
    total_current_month: Time

    def __init__(self, activity_record: pg.Record):
        self.total_current_month = Time(activity_record['current_month'])


@dataclass
class Guild:
    connection_pool: PoolWrapper = field(repr=False)
    discord_guild: discord.Guild = field(repr=False)
    guild_id: int
    guild_name: str
    channels: Channels
    roles: Roles
    currency: Currency
    features: list[str]
    reactions: list[Reaction]
    responses: Responses
    join_message: str
    leave_message: str
    level_message: str
    xp_multiplier: int
    levels_enabled: bool

    def __init__(self,
                 pool: PoolWrapper,
                 guild: discord.Guild,
                 guild_record: pg.Record,
                 channels_record: list[pg.Record],
                 features_record: list[pg.Record],
                 responses_record: list[pg.Record],
                 reaction_roles: list[pg.Record],
                 currency_total: int
                 ):
        self.connection_pool = pool
        self.discord_guild = guild
        self.guild_id = guild.id
        self.guild_name = guild.name
        self.channels = Channels(all_channels=channels_record)
        self.roles = Roles(all_roles=guild_record['roles'])
        self.currency = Currency(currency_name=guild_record['currency_name'],
                                 currency_emoji=guild_record['currency_emoji'],
                                 total=currency_total)
        self.features = [feature['feature'] for feature in features_record]
        self.reactions = [Reaction(reaction_record=record) for record in reaction_roles]
        self.responses = Responses(response_record=responses_record)
        self.join_message = guild_record['join_message']
        self.leave_message = guild_record['leave_message']
        self.level_message = guild_record['level_up_message']
        self.xp_multiplier = round(guild_record['xp_multiplier'], 2)
        self.levels_enabled = guild_record['enable_levels']

    async def get_online_players(self):
        async with self.connection_pool.connection() as conn:
            online_players = await conn.fetch("""
                                              SELECT * FROM thorny.playtime
                                              JOIN thorny.user
                                              ON thorny.user.thorny_user_id = thorny.playtime.thorny_user_id
                                              WHERE disconnect_time is NULL
                                              AND thorny.user.guild_id = $1
                                              ORDER BY connect_time DESC
                                              """,
                                              self.guild_id)

            return online_players