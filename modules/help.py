from datetime import datetime, timedelta
import discord
from discord.ext import commands
import errors
from modules import leaderboard, gateway, bank, playtime, profile


class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['hlp'], invoke_without_command=True)
    async def help(self, ctx):
        lst = []
        for cog in self.client.cogs:
            lst.append(cog)
            for command in self.client.get_cog(cog).get_commands():
                lst.append(command.name)

        await ctx.send(lst)
