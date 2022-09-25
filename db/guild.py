import asyncpg as pg
from datetime import datetime, timedelta
import discord
from thorny_core import errors
from dataclasses import dataclass, field


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
class Activity:
    ...


@dataclass
class Guild:
    connection_pool: pg.Pool = field(repr=False)
    discord_guild: discord.Guild = field(repr=False)
    guild_id: int
    guild_name: str
    channels: Channels
    roles: Roles
    currency: Currency
    exact_responses: dict
    wildcard_responses: dict
    join_message: str
    leave_message: str
    level_message: str
    xp_multiplier: int
    levels_enabled: bool

    def __init__(self,
                 pool: pg.Pool,
                 guild: discord.Guild,
                 guild_record: pg.Record,
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
        self.exact_responses = guild_record['responses_exact']
        self.wildcard_responses = guild_record['responses_wildcard']
        self.join_message = guild_record['join_message']
        self.leave_message = guild_record['leave_message']
        self.level_message = guild_record['level_up_message']
        self.xp_multiplier = guild_record['xp_multiplier']
        self.levels_enabled = guild_record['enable_levels']
