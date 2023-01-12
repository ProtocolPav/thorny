from datetime import datetime, time

import discord
from discord.ext import commands, tasks

import giphy_client
from db import UserFactory
from thorny_core.db import event as new_event
from thorny_core.uikit import embeds
import errors
import traceback
import json
import random
import sys
import httpx
from thorny_core.db.factory import GuildFactory
from thorny_core.uikit.views import PersistentProjectAdminButtons, ROAVerificationPanel
from modules import money, help, inventory, leaderboards, moderation, playtime, profile, level, setup, secret_santa

config = json.load(open('../thorny_data/config.json', 'r+'))
vers = json.load(open('version.json', 'r'))
v = vers["version"]

TOKEN = config["token"]

api_instance = giphy_client.DefaultApi()
giphy_token = config["giphy_token"]

intents = discord.Intents.all()
thorny = commands.Bot(intents=intents)
thorny.remove_command('help')
bot_started = datetime.now().replace(microsecond=0)


@thorny.event
async def on_ready():
    print(config['ascii_thorny'])
    bot_activity = discord.Activity(type=discord.ActivityType.listening,
                                    name=f"Rockin' Around Thorny | {v}")
    await thorny.change_presence(activity=bot_activity)
    print(f"[{datetime.now().replace(microsecond=0)}] [ONLINE] {thorny.user}\n"
          f"[{datetime.now().replace(microsecond=0)}] [SERVER] Running {v}")
    print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] I am in {len(thorny.guilds)} Guilds")
    thorny.add_view(PersistentProjectAdminButtons())
    thorny.add_view(ROAVerificationPanel())


@tasks.loop(seconds=500)
async def interruption_check():
    async with httpx.AsyncClient() as client:
        r = await client.get("http://169.254.169.254/latest/meta-data/spot/instance-action", timeout=None)
        if r.status_code != 404:
            pass


@tasks.loop(hours=24.0)
async def birthday_checker():
    print(f"[{datetime.now().replace(microsecond=0)}] [LOOP] Ran birthday checker loop")
    bday_list = await UserFactory.get_birthdays()
    for user in bday_list:
        for guild in thorny.guilds:
            if guild.id == user["guild_id"]:
                thorny_guild = await GuildFactory.build(guild)
                thorny_user = await UserFactory.get(guild, user['thorny_user_id'])

                birthday_event = new_event.Birthday(thorny, datetime.now(), thorny_user, thorny_guild)
                await birthday_event.log()


@tasks.loop(time=time(hour=16))
async def day_counter():
    print(f"[{datetime.now().replace(microsecond=0)}] [LOOP] Ran days counter loop")
    days_since_start = datetime.now() - datetime.strptime("2022-07-30 16:00", "%Y-%m-%d %H:%M")
    storyforge_channel = thorny.get_channel(932566162582167562)
    await storyforge_channel.send(f"*Rise and shine, Everthorn!*\n"
                                  f"**Day {days_since_start.days + 1}** has dawned upon us.")


@birthday_checker.before_loop
async def before_check():
    await thorny.wait_until_ready()


birthday_checker.start()
day_counter.start()
interruption_check.start()


@thorny.slash_command(description="Get bot stats")
async def ping(ctx):
    await ctx.respond(embed=embeds.ping_embed(thorny, bot_started))


@thorny.event
async def on_application_command_error(context: discord.ApplicationContext, exception: errors.ThornyError):
    print(f"Ignoring exception in command {context.command}:", file=sys.stderr)
    traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    command = context.command
    if command and command.has_error_handler():
        return

    cog = context.cog
    if cog and cog.has_error_handler():
        return

    try:
        await context.respond(embed=exception.return_embed(), ephemeral=True)

    except discord.NotFound:
        error = errors.UnexpectedError2(str(exception.with_traceback(exception.__traceback__)))
        await context.respond(embed=error.return_embed())

    except AttributeError:
        error = errors.UnexpectedError2(str(exception.with_traceback(exception.__traceback__)))
        await context.respond(embed=error.return_embed())


@thorny.event
async def on_message(message: discord.Message):
    if not message.author.bot:
        thorny_guild = await GuildFactory.build(message.guild)

        if message.content.lower() in thorny_guild.exact_responses:
            response_list = thorny_guild.exact_responses[message.content.lower()]
            response = response_list[random.randint(0, len(response_list) - 1)]
            await message.reply(response, allowed_mentions=discord.AllowedMentions.none())

        else:
            for invoker in thorny_guild.wildcard_responses:
                if invoker in message.content.lower():
                    response_list = thorny_guild.wildcard_responses[invoker]
                    response = response_list[random.randint(0, len(response_list) - 1)]
                    await message.reply(response, allowed_mentions=discord.AllowedMentions.none())


@thorny.listen()
async def on_message(message: discord.Message):
    if not message.author.bot:
        thorny_user = await UserFactory.build(message.author)
        thorny_guild = await GuildFactory.build(message.guild)

        if thorny_guild.levels_enabled:
            gain_xp_event = new_event.GainXP(thorny, datetime.now(), thorny_user, thorny_guild, message)

            await gain_xp_event.log()


@thorny.event
async def on_message_delete(message: discord.Message):
    if not message.author.bot and message.content is not None:
        thorny_guild = await GuildFactory.build(message.guild)

        if thorny_guild.channels.logs_channel is not None:
            logs_channel = thorny.get_channel(thorny_guild.channels.logs_channel)

            await logs_channel.send(embed=embeds.message_delete_embed(message, datetime.now()))


@thorny.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if not before.author.bot and before.content != after.content:
        thorny_guild = await GuildFactory.build(before.guild)

        if thorny_guild.channels.logs_channel is not None:
            logs_channel = thorny.get_channel(thorny_guild.channels.logs_channel)

            await logs_channel.send(embed=embeds.message_edit_embed(before, after, datetime.now()))


@thorny.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    thorny_guild = await GuildFactory.build(thorny.get_guild(payload.guild_id))

    for reaction_role in thorny_guild.reactions:
        if reaction_role.message_id == payload.message_id and reaction_role.emoji == payload.emoji.name:
            role_to_add = discord.utils.get(thorny_guild.discord_guild.roles, id=reaction_role.role_id)
            role_name_search = discord.utils.get(thorny_guild.discord_guild.roles, name=reaction_role.role_name)

            if role_to_add is None and role_name_search is not None:
                role_to_add = role_name_search
                reaction_role.role_id = role_to_add.id
                reaction_role.role_name = role_to_add.name
            elif role_name_search is None and role_to_add is not None:
                reaction_role.role_id = role_to_add.id
                reaction_role.role_name = role_to_add.name

            member = thorny_guild.discord_guild.get_member(payload.user_id)

            if role_to_add is not None and member != thorny.user:
                await member.add_roles(role_to_add)


@thorny.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    thorny_guild = await GuildFactory.build(thorny.get_guild(payload.guild_id))

    for reaction_role in thorny_guild.reactions:
        if reaction_role.message_id == payload.message_id and reaction_role.emoji == payload.emoji.name:
            role_to_add = discord.utils.get(thorny_guild.discord_guild.roles, id=reaction_role.role_id)
            role_name_search = discord.utils.get(thorny_guild.discord_guild.roles, name=reaction_role.role_name)

            if role_to_add is None and role_name_search is not None:
                role_to_add = role_name_search
                reaction_role.role_id = role_to_add.id
                reaction_role.role_name = role_to_add.name
            elif role_name_search is None and role_to_add is not None:
                reaction_role.role_id = role_to_add.id
                reaction_role.role_name = role_to_add.name

            member = thorny_guild.discord_guild.get_member(payload.user_id)

            if role_to_add is not None and member != thorny.user:
                await member.remove_roles(role_to_add)


@thorny.event
async def on_member_join(member: discord.Member):
    await UserFactory.create([member])
    thorny_user = await UserFactory.build(member)
    thorny_guild = await GuildFactory.build(member.guild)

    if thorny_guild.channels.welcome_channel is not None:
        welcome_channel = thorny.get_channel(thorny_guild.channels.welcome_channel)

        await welcome_channel.send(embed=embeds.user_join(thorny_user, thorny_guild))


@thorny.event
async def on_member_remove(member):
    await UserFactory.deactivate([member])
    thorny_user = await UserFactory.build(member)
    thorny_guild = await GuildFactory.build(member.guild)

    if thorny_guild.channels.welcome_channel is not None:
        welcome_channel = thorny.get_channel(thorny_guild.channels.welcome_channel)

        await welcome_channel.send(embed=embeds.user_leave(thorny_user, thorny_guild))


@thorny.event
async def on_guild_join(guild: discord.Guild):
    member_list = await guild.fetch_members().flatten()
    await UserFactory.create(member_list)
    await GuildFactory.create(guild)


@thorny.event
async def on_guild_remove(guild):
    member_list = guild.members
    await UserFactory.deactivate(member_list)
    await GuildFactory.deactivate(guild)


thorny.add_cog(setup.Configuration(thorny))
thorny.add_cog(moderation.Moderation(thorny))
thorny.add_cog(money.Money(thorny))
thorny.add_cog(inventory.Inventory(thorny))
thorny.add_cog(profile.Profile(thorny))
thorny.add_cog(playtime.Playtime(thorny))
thorny.add_cog(level.Level(thorny))
thorny.add_cog(leaderboards.Leaderboard(thorny))
thorny.add_cog(help.Help(thorny))

# Uncomment only during Christmastime
# thorny.add_cog(secret_santa.SecretSanta(thorny))

# asyncio.get_event_loop().run_until_complete(thorny.start(TOKEN))
thorny.run(TOKEN)
