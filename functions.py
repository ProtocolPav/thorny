import json
import os
from datetime import datetime, timedelta, date
import asyncio
import discord
import discord.ext
from dateutil import relativedelta


def calculate_reward(prize_list, prizes):
    nugs_reward = 0
    for item in prize_list:
        nugs_reward += item[1]
    if prize_list[0] != prize_list[1] != prize_list[2] != prize_list[3] and prizes[5] not in prize_list:
        nugs_reward = nugs_reward * 2
    return nugs_reward


async def generate_help_dict(self, ctx: discord.ApplicationContext):
    help_dict = {}
    for cog in self.client.cogs:
        help_dict[f"{cog}"] = []
        for command in self.client.get_cog(cog).get_commands():

            if isinstance(command, discord.SlashCommandGroup):
                for subcommand in command.walk_commands():
                    if isinstance(subcommand, discord.SlashCommand):
                        if subcommand.guild_ids is None or ctx.guild.id in subcommand.guild_ids:
                            options = ''
                            for option in subcommand.options:
                                if option.required is True:
                                    options = f"{options} `{option.name}:required`"
                                else:
                                    options = f"{options} `{option.name}:optional`"
                            help_dict[f"{cog}"].append({"name": subcommand.mention,
                                                        "desc": subcommand.description,
                                                        'usage': options})

            elif isinstance(command, discord.SlashCommand):
                if command.guild_ids is None or ctx.guild.id in command.guild_ids:
                    options = ''
                    for option in command.options:
                        if option.required is True:
                            options = f"{options} `{option.name}:required`"
                        else:
                            options = f"{options} `{option.name}:optional`"
                    help_dict[f"{cog}"].append({"name": command.mention,
                                                "desc": command.description,
                                                'usage': options})

    return help_dict
