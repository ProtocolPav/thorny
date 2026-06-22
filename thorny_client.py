import discord

from api_client import ManagedAPIClient


class ThornyBot(discord.Bot):
    api: ManagedAPIClient = ManagedAPIClient()