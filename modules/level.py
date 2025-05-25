import discord
from discord.ext import commands

import thorny_errors


class Level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="See someone's Thorny Level, as well as their rank")
    async def level(self, ctx, user: discord.Member = None):
        raise thorny_errors.UnexpectedError2("This command is disabled for now :((")

    @commands.slash_command(description="Level up a user")
    @commands.has_permissions(administrator=True)
    async def levelup(self, ctx, user: discord.Member, level: int):
        raise thorny_errors.UnexpectedError2("This command is disabled for now :((")
