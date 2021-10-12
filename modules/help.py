from datetime import datetime, timedelta
import discord
from discord.ext import commands
import errors
from modules import leaderboard, gateway, bank, playtime, profile


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['hlp'], invoke_without_command=True)
    async def help(self, ctx, cmd=None, subcmd=None):
        if cmd is None:
            dict = {}
            for cog in self.client.cogs:
                dict[f"{cog}"] = []
                for command in self.client.get_cog(cog).get_commands():
                    if isinstance(command, commands.Group):
                        dict[f"{cog}"].append(command.name)
                        for subcommand in command.walk_commands():
                            dict[f"{cog}"].append(f"{command.name} {subcommand.name}")
                    else:
                        dict[f"{cog}"].append(command.name)
            sendhelp = ''
            for cog in self.client.cogs:
                sendhelp = f"{sendhelp}\n**{cog} Commands:**\n{dict[f'{cog}']}\n"
            await ctx.send(f"**BETA**\n\n{sendhelp}")
        else:
            if subcmd is None:
                for command in self.client.commands:
                    if cmd == command.name:
                        await ctx.send(f"{ctx.prefix}{command.name} {command.signature}")
            else:
                for command in self.client.commands:
                    if cmd == command.name:
                        for subcommand in command.walk_commands():
                            if subcmd == subcommand.name:
                                await ctx.send(f"{ctx.prefix}{subcommand.name} {subcommand.signature}")
