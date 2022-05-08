import json
import os
from datetime import datetime, timedelta, date
import asyncio
import discord
import discord.ext
from dateutil import relativedelta


def get_user_kingdom(ctx, user):
    kingdom = None
    kingdoms_list = ['Stregabor', 'Ambria', 'Eireann', 'Dalvasha', 'Asbahamael']
    for item in kingdoms_list:
        if discord.utils.find(lambda r: r.name == item, ctx.guild.roles) in user.roles:
            kingdom = item.capitalize()
    return kingdom


def calculate_reward(prize_list, prizes):
    nugs_reward = 0
    for item in prize_list:
        nugs_reward += item[1]
    if prize_list[0] != prize_list[1] != prize_list[2] != prize_list[3] and prizes[5] not in prize_list:
        nugs_reward = nugs_reward * 2
    return nugs_reward


async def generate_help_dict(self, ctx):
    help_dict = {}
    for cog in self.client.cogs:
        help_dict[f"{cog}"] = []
        cmd_num = 0
        for command in self.client.get_cog(cog).get_commands():
            cmd_num += 1
            if isinstance(command, discord.SlashCommandGroup):
                for subcommand in command.walk_commands():
                    if isinstance(subcommand, discord.SlashCommand):
                        options = ''
                        for item in subcommand.options:
                            if item.required is True:
                                options = f"{options} <{item.name}>"
                            else:
                                options = f"{options} [{item.name}]"
                        if not subcommand.checks:
                            help_dict[f"{cog}"].append({"name": f"{subcommand}",
                                                        "desc": subcommand.description,
                                                        "alias": None, 'usage': options, 'example': None})
                        elif subcommand.checks and ctx.author.guild_permissions.administrator:
                            help_dict[f"{cog}"].append({"name": f"{subcommand}",
                                                        "desc": subcommand.description,
                                                        "alias": None, 'usage': options, 'example': None})
            elif isinstance(command, discord.SlashCommand):
                options = ''
                for item in command.options:
                    if item.required is True:
                        options = f"{options} <{item.name}>"
                    else:
                        options = f"{options} [{item.name}]"
                if not command.checks:
                    help_dict[f"{cog}"].append({"name": command.name,
                                                "desc": command.description,
                                                "alias": None, 'usage': options, 'example': None})
                elif command.checks and ctx.author.guild_permissions.administrator:
                    help_dict[f"{cog}"].append({"name": command.name,
                                                "desc": command.description,
                                                "alias": None, 'usage': options, 'example': None})
    return help_dict
