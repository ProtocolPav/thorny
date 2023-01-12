import discord
from discord.ext import commands
from thorny_core.uikit.views import ServerSetup
from thorny_core.db import GuildFactory


class Configuration(commands.Cog):
    def __init__(self, client):
        self.client: discord.Bot = client

    @commands.slash_command(description="Configure your server settings",
                            guild_ids=GuildFactory.get_guilds_by_feature('BETA'))
    @commands.has_permissions(administrator=True)
    async def configure(self, ctx: discord.ApplicationContext):
        await ctx.respond(view=ServerSetup(),
                          ephemeral=True)
