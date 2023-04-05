import discord
from discord.ext import commands
from thorny_core import uikit
from thorny_core.db import GuildFactory
from datetime import datetime

class Other(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot_started = datetime.now().replace(microsecond=0)

    @commands.slash_command(description="Access the Thorny Help Center",
                            guild_ids=GuildFactory.get_guilds_by_feature('BASIC'))
    async def help(self, ctx: discord.ApplicationContext):
        view = uikit.HelpDropdown(self.client, ctx.guild.id)
        for item in view.help_options:
            if item.label == "Home":
                index = view.help_options.index(item)
                view.help_options[index].default = True
            else:
                index = view.help_options.index(item)
                view.help_options[index].default = False

        await ctx.respond(embed=view.default, view=view)


    @commands.slash_command(description="Get bot stats",
                          guild_ids=GuildFactory.get_guilds_by_feature('BASIC'))
    async def ping(self, ctx):
        await ctx.respond(embed=uikit.ping_embed(self.client, self.bot_started))


    @commands.slash_command(description="Configure your server settings",
                            guild_ids=GuildFactory.get_guilds_by_feature('BETA'))
    @commands.has_permissions(administrator=True)
    async def configure(self, ctx: discord.ApplicationContext):
        await ctx.respond(view=uikit.ServerSetup(),
                          ephemeral=True)