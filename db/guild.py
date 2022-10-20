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
class Features:
    everthorn_exclusive: bool
    beta_features: bool
    premium: bool
    basic: bool

    def __init__(self, features_dict: dict):
        self.everthorn_exclusive = bool(features_dict['everthorn_only'])
        self.beta_features = bool(features_dict['beta'])
        self.premium = bool(features_dict['premium'])
        self.basic = bool(features_dict['basic'])


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
    features: Features
    reactions: list[Reaction]
    exact_responses: dict[str, list[str]]
    wildcard_responses: dict[str, list[str]]
    join_message: str
    leave_message: str
    level_message: str
    xp_multiplier: float
    levels_enabled: bool

    def __init__(self,
                 pool: pg.Pool,
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
        self.features = Features( features_dict=guild_record['features'])
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
