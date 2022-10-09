import discord
import asyncio
from discord.ext import commands
from thorny_core.uikit.views import ProjectApplicationForm
from thorny_core.db import GuildFactory


class Applications(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Apply for a Project!",
                            guild_ids=GuildFactory.get_everthorn_exclusive_guilds())
    async def apply(self, ctx: discord.ApplicationContext):
        await ctx.respond(view=ProjectApplicationForm(ctx),
                          ephemeral=True)
