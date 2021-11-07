import asyncio
import random
from datetime import datetime

import discord
from discord.ext import commands, tasks

from functions import profile_update, profile_change_months, birthday_announce, tip_send
import errors
import json
from modules import leaderboard, gateway, bank, playtime, profile, help, fun, inventory

config_file = open('../thorny_data/config.json', 'r+')
config = json.load(config_file)
version_json = json.load(open('version.json', 'r'))
v = version_json["version"]

ans = input("Are You Running Thorny (t) or Development Thorny (d)?\n")
if ans == 't':
    TOKEN = config["token"]
elif ans == 'd':
    TOKEN = config["dev_token"]
else:
    print('This is not a valid Token. Please run the program again.')

thorny = commands.Bot(command_prefix='!', case_insensitive=True)
thorny.remove_command('help')


@thorny.event
async def on_ready():
    print(f"[ONLINE] {thorny.user}\nRunning {v}\nDate is {datetime.now()}")
    bot_activity = discord.Activity(type=discord.ActivityType.watching,
                                    name=f"for !help | {v}")
    await thorny.change_presence(activity=bot_activity)
    await profile_change_months()


@thorny.command()
async def update(ctx, user: discord.User, key1, *value):
    print(user, key1, value)
    profile_update(user, ','.join(value), key1)
    await ctx.send(f"Updated {user}'s {key1} to be {value}")


@thorny.command()
async def version(ctx):
    await ctx.send(f"I am Thorny. I'm currently on {v}! I love travelling around the world and right now I'm at "
                   f"{version_json['nickname']}")


@thorny.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    thorny.command_prefix = prefix
    await ctx.send(f"Prefix changed to `{prefix}`")


@thorny.event
async def on_message(message):
    if message.content.lower() == 'hello':
        await message.channel.send("Hi!")
    elif message.content.lower() == 'pav':
        await message.channel.send('Yes. He is Pav.')
    elif message.content.lower() == '<@!879249190801248276>':
        await message.channel.send('Use !gateway for help!')

    await thorny.process_commands(message)  # Not putting this on on_message breaks all .command()


@thorny.event
async def on_member_join(member):
    profile_update(member, datetime.now(), 'date_joined')


thorny.add_cog(bank.Bank(thorny))
thorny.add_cog(leaderboard.Leaderboard(thorny))
thorny.add_cog(inventory.Inventory(thorny))
thorny.add_cog(gateway.Gateway(thorny))
thorny.add_cog(profile.Profile(thorny))
thorny.add_cog(help.Help(thorny))
#thorny.add_cog(fun.Fun(thorny))
thorny.add_cog(playtime.Activity(thorny))  # Do this for every cog. This can also be changed through commands.
thorny.run(TOKEN)
