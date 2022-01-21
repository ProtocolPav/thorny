from datetime import datetime

import discord
from discord.ext import commands

import functions as func
import logs
import dbutils
import json
import asyncio
from modules import bank, gateway, help, inventory, leaderboard, playtime, profile, moderation

config = json.load(open('../thorny_data/config.json', 'r+'))
vers = json.load(open('version.json', 'r'))
v = vers["version"]

ans = input("Are You Running Thorny (t) or Development Thorny (d)?\n")
if ans == 't':
    TOKEN = config["token"]
elif ans == 'd':
    TOKEN = config["dev_token"]

intents = discord.Intents.all()
thorny = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
thorny.remove_command('help')


@thorny.event
async def on_ready():
    bot_activity = discord.Activity(type=discord.ActivityType.watching,
                                    name=f"you... | {v}")
    print(f"[ONLINE] {thorny.user}\n[INFO]   Running {v}\n[INFO]   Date is {datetime.now()}")
    await thorny.change_presence(activity=bot_activity)
    await func.update_months(thorny)


@thorny.command(aliases=['version'])
async def ping(ctx):
    await ctx.send(f"I am Thorny. I'm currently on {v}! I love travelling around the world and right now I'm at "
                   f"{vers['nickname']}\n**Ping:** {round(thorny.latency, 3)}s")


@thorny.command()
async def changelog(ctx, ver=v):
    if ver in vers['changelogs']:
        await ctx.send(f"Changelog for {ver}:\n\n{vers['changelogs'][ver]}")
    else:
        await ctx.send(f"I am Thorny. I'm currently on {v}! You asked to see {ver}, which doesn't exist")


@thorny.event
async def on_message(message):
    if message.content.lower() == 'hello':
        await message.channel.send("Hi!")
    elif message.content.lower() == 'pav':
        await message.channel.send('Yes. He is Pav.')
    elif message.content.lower() == 'yesss':
        await message.channel.send('WOOOOOOOO!!!!!')
    elif 'scream' in message.content.lower():
        await message.channel.send('AAAHHHHHHHHHH')

    await thorny.process_commands(message)  # Not putting this on on_message breaks all .command()


@thorny.listen()
async def on_message(message):
    banned_words = ['nigga', 'nigg', 'nigger', 'fag', 'faggot', 'shota', 'f*g', 'n*gg']
    for word in banned_words:
        if word in message.content.lower():
            await message.delete()


@thorny.event
async def on_message_delete(message):
    log_embed = logs.message_delete(message)
    stafflogs = thorny.get_channel(config['channels']['event_logs'])
    await stafflogs.send(embed=log_embed)


@thorny.event
async def on_message_edit(before, after):
    log_embed = logs.message_edit(before, after)
    stafflogs = thorny.get_channel(config['channels']['event_logs'])
    await stafflogs.send(embed=log_embed)


@thorny.event
async def on_raw_reaction_add(payload):
    guild = thorny.get_guild(payload.guild_id)
    male = discord.utils.get(guild.roles, name="He/Him")
    female = discord.utils.get(guild.roles, name="She/Her")
    other = discord.utils.get(guild.roles, name="They/Them")
    if payload.message_id == config['channels']['pronoun_message_id']:
        if payload.emoji.name == '👱':
            member = guild.get_member(payload.user_id)
            await member.add_roles(other)
        elif payload.emoji.name == '👨‍🦱':
            member = guild.get_member(payload.user_id)
            await member.add_roles(male)
        elif payload.emoji.name == '👩‍🦰':
            member = guild.get_member(payload.user_id)
            await member.add_roles(female)


@thorny.event
async def on_raw_reaction_remove(payload):
    guild = thorny.get_guild(payload.guild_id)
    male = discord.utils.get(guild.roles, name="He/Him")
    female = discord.utils.get(guild.roles, name="She/Her")
    other = discord.utils.get(guild.roles, name="They/Them")
    if payload.message_id == config['channels']['pronoun_message_id']:
        if payload.emoji.name == '👱':
            member = guild.get_member(payload.user_id)
            await member.remove_roles(other)
        elif payload.emoji.name == '👨‍🦱':
            member = guild.get_member(payload.user_id)
            await member.remove_roles(male)
        elif payload.emoji.name == '👩‍🦰':
            member = guild.get_member(payload.user_id)
            await member.remove_roles(female)


@thorny.event
async def on_member_join(member):
    func.profile_update(member, f'{datetime.now().replace(microsecond=0)}', 'date_joined')
    print(f"{member} joined")
    await gateway.Information.new(thorny, member)


@thorny.event
async def on_guild_join(guild):
    print("I joined" + guild)


thorny.add_cog(bank.Bank(thorny))
thorny.add_cog(leaderboard.Leaderboard(thorny))
thorny.add_cog(inventory.Item(thorny))
thorny.add_cog(gateway.Information(thorny))
thorny.add_cog(profile.Profile(thorny))
thorny.add_cog(help.Help(thorny))
thorny.add_cog(moderation.Moderation(thorny))
#thorny.add_cog(fun.Fun(thorny))
thorny.add_cog(playtime.Playtime(thorny))  # Do this for every cog. This can also be changed through commands.
thorny.run(TOKEN)
