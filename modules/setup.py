import discord
from discord.ext import commands
from thorny_core.uikit.views import ServerSetup


class Configurations(commands.Cog):
    def __init__(self, client):
        self.client: discord.Bot = client

    @commands.slash_command(description="Configure your server settings")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx: discord.ApplicationContext):
        await ctx.respond(view=ServerSetup(),
                          ephemeral=True)
