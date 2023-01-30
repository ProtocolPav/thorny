import asyncpg as pg
from datetime import datetime, timedelta, date
import discord
from thorny_core.db.poolwrapper import PoolWrapper
from dataclasses import dataclass, field


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
    logs_channel: int
    welcome_channel: int
    gulag_channel: int
    projects_channel: int
    announcements_channel: int
    thorny_updates_channel: int

    def __init__(self, all_channels: dict):
        self.logs_channel = all_channels['logs']
        self.welcome_channel = all_channels['welcome']
        self.gulag_channel = all_channels['gulag']
        self.projects_channel = all_channels['projects']
        self.announcements_channel = all_channels['announcements']
        self.thorny_updates_channel = all_channels['thorny_updates']


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
    features_v2: list[str]
    reactions: list[Reaction]
    exact_responses: dict[str, list[str]]
    wildcard_responses: dict[str, list[str]]
    join_message: str
    leave_message: str
    level_message: str
    xp_multiplier: int
    levels_enabled: bool

    def __init__(self,
                 pool: PoolWrapper,
                 guild: discord.Guild,
                 guild_record: pg.Record,
                 reaction_roles: list[pg.Record],
                 currency_total: int
                 ):
        self.connection_pool = pool
        self.discord_guild = guild
        self.guild_id = guild.id
        self.guild_name = guild.name
        self.channels = Channels(all_channels=guild_record['channels'])
        self.roles = Roles(all_roles=guild_record['roles'])
        self.currency = Currency(currency_name=guild_record['currency_name'],
                                 currency_emoji=guild_record['currency_emoji'],
                                 total=currency_total)
        self.features_v2 = guild_record['features_v2']
        self.reactions = []
        self.exact_responses = guild_record['responses_exact']
        self.wildcard_responses = guild_record['responses_wildcard']
        self.join_message = guild_record['join_message']
        self.leave_message = guild_record['leave_message']
        self.level_message = guild_record['level_up_message']
        self.xp_multiplier = round(guild_record['xp_multiplier'], 2)
        self.levels_enabled = guild_record['enable_levels']

        for record in reaction_roles:
            self.reactions.append(Reaction(reaction_record=record))

    async def get_online_players(self):
        async with self.connection_pool.connection() as conn:
            online_players = await conn.fetch("""
                                              SELECT * FROM thorny.activity 
                                              JOIN thorny.user
                                              ON thorny.user.thorny_user_id = thorny.activity.thorny_user_id
                                              WHERE disconnect_time is NULL
                                              AND thorny.user.guild_id = $1
                                              ORDER BY connect_time DESC
                                              """,
                                              self.guild_id)

            return online_players