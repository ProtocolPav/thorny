from datetime import datetime, timedelta

import discord
from discord.ext import commands

import giphy_client
from dbfactory import ThornyFactory
import dbevent as ev
from dbevent import Event
import json
import random
from modules import bank, help, information, inventory, leaderboard, moderation, playtime, profile, level

config = json.load(open('../thorny_data/config.json', 'r+'))
vers = json.load(open('version.json', 'r'))
v = vers["version"]

api_instance = giphy_client.DefaultApi()
giphy_token = "PYTVyPc9klW4Ej3ClWz9XFCo1TQOp72b"

ans = input("Are You Running Thorny (t) or Development Thorny (d)?\n")
if ans == 't':
    TOKEN = config["token"]
else:
    TOKEN = config["dev_token"]

intents = discord.Intents.all()
thorny = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
thorny.remove_command('help')


@thorny.event
async def on_ready():
    bot_activity = discord.Activity(type=discord.ActivityType.watching,
                                    name=f"you... | {v}")
    print(f"[ONLINE] {thorny.user}\n[SERVER] Running {v}\n[SERVER] Date is {datetime.now()}")
    await thorny.change_presence(activity=bot_activity)
    print(f"[SERVER] I am in {len(thorny.guilds)} Guilds")


@thorny.slash_command()
async def ping(ctx):
    await ctx.respond(f"I am Thorny. I'm currently on {v}! I love travelling around the world and right now I'm at "
                      f"{vers['nickname']}\n**Ping:** {round(thorny.latency, 3)}s")


@thorny.command()
async def changelog(ctx, ver=v):
    if ver in vers['changelogs']:
        await ctx.send(f"Changelog for {ver}:\n\n{vers['changelogs'][ver]}")
    else:
        await ctx.send(f"I am Thorny. I'm currently on {v}! You asked to see {ver}, which doesn't exist")


@thorny.event
async def on_message(message):
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

    if message.content.startswith('!'):
        await message.channel.send("*Hint: Maybe this command works with a `/` prefix?*\n"
                                   "*This message will be going away soon, so learn the commands!*")


@thorny.listen()
async def on_message(message):
    banned_words = config['banned_words']
    for word in banned_words:
        if word in message.content.lower() and message.author != thorny.user:
            await message.delete()


@thorny.listen()
async def on_message(message: discord.Message):
    if message.author != thorny.user:
        thorny_user = await ThornyFactory.build(message.author)
        if datetime.now() - thorny_user.counters.level_last_message > timedelta(minutes=1):
            event: Event = await ev.fetch(ev.GainXP, thorny_user, thorny)
            data = await event.log_event_in_database()
            if data.level_up:
                api_response = api_instance.gifs_search_get(giphy_token, f"{data.user.profile.level}", limit=5)
                gifs_list = list(api_response.data)
                gif = random.choice(gifs_list)

                level_up_embed = discord.Embed(colour=message.author.colour)
                level_up_embed.set_author(name=message.author, icon_url=message.author.display_avatar.url)
                level_up_embed.add_field(name=f":partying_face: Congrats!",
                                         value=f"You leveled up to **Level {data.user.profile.level}!**\n"
                                               f"Keep chatting and maybe, just maybe, you'll beat the #1")
                level_up_embed.set_image(url=gif.images.original.url)
                await message.channel.send(embed=level_up_embed)


@thorny.event
async def on_message_delete(message: discord.Message):
    if message.author != thorny.user:
        thorny_user = await ThornyFactory.build(message.author)
        event: Event = await ev.fetch(ev.MessageDelete, thorny_user, thorny)
        event.metadata.deleted_message = message
        await event.log_event_in_discord()


@thorny.event
async def on_message_edit(before, after):
    if before.author != thorny.user:
        thorny_user = await ThornyFactory.build(before.author)
        event: Event = await ev.fetch(ev.MessageEdit, thorny_user, thorny)
        event.metadata.message_before = before
        event.metadata.message_after = after
        await event.log_event_in_discord()


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
    await ThornyFactory.create([member])


@thorny.event
async def on_member_remove(member):
    await ThornyFactory.deactivate([member])


@thorny.event
async def on_guild_join(guild):
    print(f"I joined {guild.name}")
    member_list = await guild.fetch_members().flatten()
    await ThornyFactory.create(member_list)


@thorny.event
async def on_guild_remove(guild):
    print(f"I left {guild.name}")
    member_list = guild.members
    await ThornyFactory.deactivate(member_list)

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
