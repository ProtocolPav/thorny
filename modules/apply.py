import discord
from discord.ext import commands
from thorny_core.uikit.views import ProjectApplicationForm


class Applications(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Apply for a Project!",
                            guild_ids=[1023300252805103626, 611008530077712395])
    async def apply(self, ctx: discord.ApplicationContext):
        await ctx.respond(view=ProjectApplicationForm(ctx),
                          ephemeral=True)
