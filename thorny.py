import random
from datetime import datetime

import discord
from discord.ext import commands

from activity import write_log, process_json, total_json, reset_values
from activity import profile_update
from lottery import create_ticket, winners
import errors
import asyncio
import json
from thornyv1_3.modules import gateway, playtime, bank, leaderboard, profile

config_file = open('config.json', 'r+')
config = json.load(config_file)
v = config["version"]
# This token is for the TEST bot
TOKEN = "ODc5MjQ5MTkwODAxMjQ4Mjc2.YSM-ng.l_rYiSIvBFyuKxvgGmXefZqQR9k"
TOKEN_Thorny = "ODY3ODE1Mzk4MjA0MTEyOTE3.YPmmEg.N28SIdOPgEIyLxojDp4nHKh9MvE"
thorny = commands.Bot(command_prefix='!')


@thorny.event
async def on_ready():
    print(f"[ONLINE] {thorny.user}\nRunning {v}\nDate is {datetime.now()}")
    bot_activity = discord.Activity(type=discord.ActivityType.watching,
                                    name=f"you | {v}")
    await thorny.change_presence(activity=bot_activity)


class Store(commands.Cog):
    def __init__(self, client):
        self.client = client
    available_items = ['Empty', 'Ticket', 'Custom Role 1m']

    @commands.group(aliases=['inv'], invoke_without_command=True)
    async def inventory(self, ctx, user: discord.Member = None):
        inventory_list = ''
        number = 0
        profile_json = json.load(open('text files/profiles.json', 'r'))
        if user is None:
            person = ctx.author
        else:
            person = user
        for slot in range(1,7):
            number += 1
            inventory_list = f'{inventory_list}:small_orange_diamond: ' \
                             f'{profile_json[f"{person.id}"]["inventory"][f"slot{number}"]} **|** ' \
                             f'{profile_json[f"{person.id}"]["inventory"][f"slot{number}_amount"]}\n'
        await ctx.send(f"**{person}'s Inventory**\n{inventory_list}")

    @inventory.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, user: discord.User=None, item=None, amnt=1):
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        item_placed = False
        slot = 0

        if item.lower() == 'role' or item.lower() == 'custom':
            while not item_placed:
                slot += 1
                if profile[f"{user.id}"]['inventory'][f'slot{slot}'] == 'Empty' or \
                   profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == "Custom Role 1m":
                    profile_update(user, 'Custom Role 1m', 'inventory', f'slot{slot}')
                    amnt = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}_amount'] + int(amnt)
                    profile_update(user, amnt, 'inventory', f'slot{slot}_amount')
                    item_placed = True
                    await ctx.send(f'Added item {item} to slot {slot}')
                else:
                    pass
        elif item.lower() == 'ticket' or item.lower() == 'lottery':
            while not item_placed:
                slot += 1
                if profile[f"{user.id}"]['inventory'][f'slot{slot}'] == 'Empty' or \
                   profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == "Ticket":
                    profile_update(user, 'Ticket', 'inventory', f'slot{slot}')
                    amnt = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}_amount'] + int(amnt)
                    profile_update(user, amnt, 'inventory', f'slot{slot}_amount')
                    item_placed = True
                    await ctx.send(f'Added item {item} to slot {slot}')
                else:
                    pass

    @inventory.command()
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, user:discord.User=None, item=None):
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        item_removed = False
        slot = 0

        if item.lower() == 'role' or item.lower() == 'custom':
            while not item_removed:
                slot += 1
                if profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == "Custom Role 1m":
                    profile_update(user, 'Empty', 'inventory', f'slot{slot}')
                    profile_update(user, 0, 'inventory', f'slot{slot}_amount')
                    item_removed = True
                    await ctx.send(f'Removed item {item} from slot {slot}')
                else:
                    pass
        elif item.lower() == 'ticket' or item.lower() == 'lottery':
            while not item_removed:
                slot += 1
                if profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == "Ticket":
                    profile_update(user, 'Empty', 'inventory', f'slot{slot}')
                    profile_update(user, 0, 'inventory', f'slot{slot}_amount')
                    item_removed = True
                    await ctx.send(f'Removed item {item} from slot {slot}')
                else:
                    pass

    @commands.group(invoke_without_command=True)
    async def store(self, ctx):
        await ctx.send('Items in the Store:\n'
                       'Lottery Ticket - 10n\n'
                       'Use !store buy item to buy an item!')

    @store.command()
    async def buy(self, ctx, item):
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        item_placed = False
        slot = 0

        if item.lower() == 'ticket' or item.lower() == 'lottery':
            if 18 <= int(datetime.now().strftime("%d")) <= 25:
                newbal = profile[f"{ctx.author.id}"]['balance'] - 10
                profile_update(ctx.author, newbal, 'balance')
                while not item_placed:
                    slot += 1
                    if profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == 'Empty' or \
                       profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}'] == 'Ticket':
                        amnt = profile[f"{ctx.author.id}"]['inventory'][f'slot{slot}_amount'] + 1
                        profile_update(ctx.author, 'Ticket', 'inventory', f'slot{slot}')
                        profile_update(ctx.author, amnt, 'inventory', f'slot{slot}_amount')
                        item_placed = True
                        ticket_number = create_ticket(ctx.author, 1)
                        await ctx.send('Bought a ticket!')
                        await ctx.author.send(f"Your ticket is {ticket_number}")
                    else:
                        pass
            else:
                await ctx.send(embed=errors.Shop.ticket_buy_error)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def getwinners(self, ctx):
        winners_list = winners(thorny)
        await ctx.send(winners_list)


@thorny.command()
async def update(ctx, user: discord.User, key1, *value):
    print(user, key1, value)
    profile_update(user, ','.join(value), key1)
    await ctx.send(f"Updated {user}'s {key1} to be {value}")


@thorny.command()
async def version(ctx):
    await ctx.send(f"Yeehaw! Howdy there boss. I am on version {v}. Isn't that coolio!")


@thorny.command(aliases=['shout', 'aaa', 'scr'])
async def scream(ctx):
    screams = ['AAAaaaAaaaAAaaaAAAAAaAAaAAAAAaaAA', 'ARGHHHHHHHHHHHHHHHHHHHHhhhhhhhh', 'GAH!',
               'ROOOOoooOOOOAARRRRRRRRRR',
               '*screams*', 'https://tenor.com/view/scream-yell-mad-angry-fury-gif-3864070',
               'GASPPPPPP AAAAAAAAAAAA']
    screamnumber = random.randint(0, 5)
    await ctx.send(f'{screams[screamnumber]}\n{ctx.author.mention}, you scared me!!!')


@thorny.command()
async def setprefix(ctx, prefix):
    if ctx.author.id == 266202793143042048:
        thorny.command_prefix = prefix
        await ctx.send(f"Prefix changed to `{prefix}`")


@thorny.command()
async def activity(ctx):
    await ctx.send('Hey! The command has changed! It is now !leaderboard (or !lb) activity')


@thorny.command()
async def nugs(ctx):
    await ctx.send('Hey! The command has changed! It is now !leaderboard (or !lb) nugs')


@thorny.command()
async def treasuries(ctx):
    await ctx.send('Hey! The command has changed! It is now !leaderboard (or !lb) treasuries')


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
    profile_update(member, datetime.now().strftime("%B %d, %Y, %H:%M:%S"), 'date_joined')


thorny.add_cog(bank.Bank(thorny))
thorny.add_cog(leaderboard.Leaderboards(thorny))
thorny.add_cog(Store(thorny))
thorny.add_cog(gateway.Gateway(thorny))
thorny.add_cog(profile.Profile(thorny))
thorny.add_cog(playtime.Activity(thorny))  # Do this for every cog. This can also be changed through commands.
thorny.run(TOKEN)
