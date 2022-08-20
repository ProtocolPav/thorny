import asyncio
from datetime import datetime, timedelta, time, timezone

import discord
from discord.ext import commands, tasks

import giphy_client
from db import UserFactory
from dbutils import User
import dbevent as ev
from dbevent import Event
import errors
import traceback
import json
import random
import sys
from modules import bank, help, information, inventory, leaderboard, moderation, playtime, profile, level, setup

config = json.load(open('../thorny_data/config.json', 'r+'))
vers = json.load(open('version.json', 'r'))
v = vers["version"]

print(
    """
     _____ _
    /__   \ |__   ___  _ __ _ __  _   _
      / /\/ '_ \ / _ \| '__| '_ \| | | |
     / /  | | | | (_) | |  | | | | |_| |
     \/   |_| |_|\___/|_|  |_| |_|\__, |
                                  |___/
        """)
# ans = input("Are You Running Thorny (t) or Development Thorny (d)?\n")
# if ans == 't':
#     TOKEN = config["token"]
# else:
#     TOKEN = config["dev_token"]
TOKEN = config["dev_token"]

api_instance = giphy_client.DefaultApi()
giphy_token = config["giphy_token"]

intents = discord.Intents.all()
thorny = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
thorny.remove_command('help')


@thorny.event
async def on_ready():
    bot_activity = discord.Activity(type=discord.ActivityType.listening,
                                    name=f"Relaxing Thorns [1 HOUR] | {v}")
    print(f"[{datetime.now().replace(microsecond=0)}] [ONLINE] {thorny.user}\n"
          f"[{datetime.now().replace(microsecond=0)}] [SERVER] Running {v}")
    await thorny.change_presence(activity=bot_activity)
    print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] I am in {len(thorny.guilds)} Guilds")


@tasks.loop(hours=24.0)
async def birthday_checker():
    print(f"[{datetime.now().replace(microsecond=0)}] [LOOP] Ran birthday checker loop")
    bday_list = await User().select_birthdays()
    for user in bday_list:
        if user["birthday"].day == datetime.now().day:
            if user["birthday"].month == datetime.now().month:
                for guild in thorny.guilds:
                    if guild.id == user["guild_id"]:
                        member = guild.get_member(user["user_id"])
                        thorny_user = await UserFactory.build(member)

                        event: Event = await ev.fetch(ev.Birthday, thorny_user, thorny)
                        await event.log_event_in_discord()


@tasks.loop(time=time(hour=16))
async def day_counter():
    print(f"[{datetime.now().replace(microsecond=0)}] [LOOP] Ran days counter loop")
    days_since_start = datetime.now() - datetime.strptime("2022-07-30 16:00", "%Y-%m-%d %H:%M")
    channel = thorny.get_channel(805722487261888522)
    await channel.send(f"*Rise and shine, Everthorn!*\n"
                       f"**Day {days_since_start.days}** has dawned upon us.")


@birthday_checker.before_loop
async def before_check():
    await thorny.wait_until_ready()

birthday_checker.start()
day_counter.start()


@thorny.slash_command()
async def ping(ctx):
    await ctx.respond(f"I am Thorny. I'm currently on {v}! **Ping:** {round(thorny.latency, 3)}s")


@thorny.event
async def on_application_command_error(context: discord.ApplicationContext, exception: Exception):
    command = context.command
    if command and command.has_error_handler():
        return

    cog = context.cog
    if cog and cog.has_error_handler():
        return

    print(f"Ignoring exception in command {context.command}:", file=sys.stderr)
    traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    if isinstance(exception, errors.ThornyError):
        try:
            await context.respond(embed=exception.return_embed(), ephemeral=True)
        except discord.NotFound:
            await context.channel.send(embed=exception.return_embed())
    elif isinstance(exception, discord.ApplicationCommandInvokeError):
        error = errors.UnexpectedError2(str(exception.with_traceback(exception.__traceback__)))
        try:
            await context.respond(embed=error.return_embed(), ephemeral=True)
        except discord.NotFound:
            await context.channel.send(embed=error.return_embed())
    else:
        error = errors.UnexpectedError1(str(exception.with_traceback(exception.__traceback__)))
        try:
            await context.respond(embed=error.return_embed())
        except discord.NotFound:
            await context.channel.send(embed=error.return_embed())


@thorny.event
async def on_message(message):
    # This event listens for keywords and responds with them
    exact = config['exact_responses']
    wildcard = config['wildcard_responses']
    if message.author != thorny.user:
        if message.content.lower() in exact:
            response_list = exact[message.content.lower()]
            response = response_list[random.randint(0, len(response_list) - 1)]
            await message.channel.send(response)
        else:
            for invoker in wildcard:
                if invoker in message.content.lower():
                    response_list = wildcard[invoker]
                    response = response_list[random.randint(0, len(response_list) - 1)]
                    await message.channel.send(response)


@thorny.listen()
async def on_message(message: discord.Message):
    # This event listens for messages and gives the user XP
    if message.author != thorny.user:
        thorny_user = await UserFactory.build(message.author)
        if datetime.now() - thorny_user.counters.level_last_message > timedelta(minutes=1):
            event: Event = await ev.fetch(ev.GainXP, thorny_user, thorny)
            data = await event.log_event_in_database()
            if data.level_up:
                event.edit_metadata("level_up_message", message)
                await event.log_event_in_discord()


@thorny.event
async def on_message_delete(message: discord.Message):
    if message.author != thorny.user:
        thorny_user = await UserFactory.build(message.author)
        event: Event = await ev.fetch(ev.MessageDelete, thorny_user, thorny)
        event.metadata.deleted_message = message
        await event.log_event_in_discord()


@thorny.event
async def on_message_edit(before, after):
    if before.author != thorny.user:
        thorny_user = await UserFactory.build(before.author)
        event: Event = await ev.fetch(ev.MessageEdit, thorny_user, thorny)
        event.metadata.message_before = before
        event.metadata.message_after = after
        await event.log_event_in_discord()


@thorny.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    guild = thorny.get_guild(payload.guild_id)
    male = discord.utils.get(guild.roles, name="He/Him")
    female = discord.utils.get(guild.roles, name="She/Her")
    other = discord.utils.get(guild.roles, name="They/Them")

    knight = discord.utils.get(guild.roles, name="Knight")
    builder = discord.utils.get(guild.roles, name="Builder")
    redstoner = discord.utils.get(guild.roles, name="Stoner")
    merchant = discord.utils.get(guild.roles, name="Merchant")
    gatherer = discord.utils.get(guild.roles, name="Gatherer")

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

    elif payload.message_id == 989073514315264070:
        if payload.emoji.name == "Knight":
            member = guild.get_member(payload.user_id)
            await member.add_roles(knight)
        elif payload.emoji.name == "Builder":
            member = guild.get_member(payload.user_id)
            await member.add_roles(builder)
        elif payload.emoji.name == "Stoner":
            member = guild.get_member(payload.user_id)
            await member.add_roles(redstoner)
        elif payload.emoji.name == "Merchant":
            member = guild.get_member(payload.user_id)
            await member.add_roles(merchant)
        elif payload.emoji.name == "Gatherer":
            member = guild.get_member(payload.user_id)
            await member.add_roles(gatherer)


@thorny.event
async def on_raw_reaction_remove(payload):
    guild = thorny.get_guild(payload.guild_id)
    male = discord.utils.get(guild.roles, name="He/Him")
    female = discord.utils.get(guild.roles, name="She/Her")
    other = discord.utils.get(guild.roles, name="They/Them")

    knight = discord.utils.get(guild.roles, name="Knight")
    builder = discord.utils.get(guild.roles, name="Builder")
    redstoner = discord.utils.get(guild.roles, name="Stoner")
    merchant = discord.utils.get(guild.roles, name="Merchant")
    gatherer = discord.utils.get(guild.roles, name="Gatherer")

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

    elif payload.message_id == 997595962933522482:
        if payload.emoji.name == "Knight":
            member = guild.get_member(payload.user_id)
            await member.remove_roles(knight)
        elif payload.emoji.name == "Builder":
            member = guild.get_member(payload.user_id)
            await member.remove_roles(builder)
        elif payload.emoji.name == "Stoner":
            member = guild.get_member(payload.user_id)
            await member.remove_roles(redstoner)
        elif payload.emoji.name == "Merchant":
            member = guild.get_member(payload.user_id)
            await member.remove_roles(merchant)
        elif payload.emoji.name == "Gatherer":
            member = guild.get_member(payload.user_id)
            await member.remove_roles(gatherer)


@thorny.event
async def on_member_join(member: discord.Member):
    await UserFactory.create([member])
    thorny_user = await UserFactory.build(member)
    event: Event = await ev.fetch(ev.UserJoin, thorny_user, thorny)
    if member.guild.id == 611008530077712395:
        await event.log_event_in_discord()


@thorny.event
async def on_member_remove(member):
    thorny_user = await UserFactory.build(member)
    event: Event = await ev.fetch(ev.UserLeave, thorny_user, thorny)
    if member.guild.id == 611008530077712395:
        await event.log_event_in_discord()
    await UserFactory.deactivate([member])


@thorny.event
async def on_guild_join(guild):
    member_list = await guild.fetch_members().flatten()
    await UserFactory.create(member_list)


@thorny.event
async def on_guild_remove(guild):
    member_list = guild.members
    await UserFactory.deactivate(member_list)


thorny.add_cog(bank.Bank(thorny))
thorny.add_cog(leaderboard.Leaderboard(thorny))
thorny.add_cog(inventory.Inventory(thorny))
thorny.add_cog(information.Information(thorny))
thorny.add_cog(profile.Profile(thorny))
thorny.add_cog(moderation.Moderation(thorny))
thorny.add_cog(playtime.Playtime(thorny))
thorny.add_cog(level.Level(thorny))
thorny.add_cog(help.Help(thorny))  # Do this for every cog. This can also be changed through commands.

thorny.run(TOKEN)
