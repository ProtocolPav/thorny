from datetime import datetime, time

import discord
from discord.ext import commands, tasks

import giphy_client
from thorny_core import nexus
from thorny_core import thorny_errors
import traceback
import json
import sys
import httpx
import modules
import uikit

config = json.load(open('../thorny_data/config.json', 'r+'))
vers = json.load(open('version.json', 'r'))
v = vers["version"]

TOKEN = config["token"]

api_instance = giphy_client.DefaultApi()
giphy_token = config["giphy_token"]

intents = discord.Intents.all()
thorny = commands.Bot(intents=intents)
thorny.remove_command('help')

shutdown_notice_received = False


@thorny.event
async def on_ready():
    print('\033[1;32m' + config['ascii_thorny'] + '\033[0m')
    bot_activity = discord.Activity(type=discord.ActivityType.watching,
                                    name=f"everything.")
    await thorny.change_presence(activity=bot_activity)
    print(f"[{datetime.now().replace(microsecond=0)}] [ONLINE] {thorny.user}\n"
          f"[{datetime.now().replace(microsecond=0)}] [SERVER] Running {v}")
    print(f"[{datetime.now().replace(microsecond=0)}] [SERVER] I am in {len(thorny.guilds)} Guilds")
    thorny.add_view(uikit.PersistentProjectAdminButtons())


# @tasks.loop(hours=24.0)
# async def birthday_checker():
#     print(f"[{datetime.now().replace(microsecond=0)}] [LOOP] Ran birthday checker loop")
#     upcoming_bdays = await generator.upcoming_birthdays(pool=poolwrapper.pool_wrapper)
#     for user in upcoming_bdays:
#         for guild in thorny.guilds:
#             if guild.id == user["guild_id"] and datetime.now().date().replace(year=2000) == user['birthday'].replace(year=2000):
#                 thorny_guild = await GuildFactory.build(guild)
#                 thorny_user = await UserFactory.fetch_by_id(thorny_guild, user['thorny_user_id'])
#
#                 birthday_event = event.Birthday(thorny, datetime.now(), thorny_user, thorny_guild)
#                 await birthday_event.log()
#
# @birthday_checker.before_loop
# async def before_check():
#     await thorny.wait_until_ready()


@tasks.loop(time=time(hour=16))
async def day_counter():
    print(f"[{datetime.now().replace(microsecond=0)}] [LOOP] Ran days counter loop")
    days_since_start = datetime.now() - datetime.strptime("2022-07-30 16:00", "%Y-%m-%d %H:%M")
    storyforge_channel = thorny.get_channel(932566162582167562)
    if (days_since_start.days + 1) % 10 == 0:
        await storyforge_channel.send(f"*Rise and shine, Everthorn!*\n"
                                      f"**Day {days_since_start.days + 1}** has dawned upon us.")


@thorny.event
async def on_application_command_error(context: discord.ApplicationContext, exception: thorny_errors.ThornyError):
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
        error = thorny_errors.UnexpectedError2(str(exception.with_traceback(exception.__traceback__)))
        await context.respond(embed=error.return_embed())

    except AttributeError:
        error = thorny_errors.UnexpectedError2(str(exception.with_traceback(exception.__traceback__)))
        await context.respond(embed=error.return_embed())


@thorny.listen()
async def on_message(message: discord.Message):
    if not message.author.bot:
        thorny_user = await nexus.ThornyUser.build(message.author)
        thorny_guild = await nexus.ThornyGuild.build(message.guild)

        if thorny_guild.has_feature('levels'):
            level_up = await thorny_user.level_up(thorny_guild.xp_multiplier)
            if level_up:
                await message.channel.send(embed=uikit.level_up_embed(thorny_user, thorny_guild))

        if message.channel.id == thorny_guild.get_channel_id('thorny_updates') and message.content:
            if 'http' not in message.content:
                async with httpx.AsyncClient() as client:
                    r = await client.get(f"http://amethyst:8000/commands/message", timeout=None,
                                         params={'msg': f'§l§8[§r§5Discord§l§8]§r §7{message.author.name}:§r {message.content}'})


@thorny.event
async def on_message_delete(message: discord.Message):
    if not message.author.bot and message.content is not None:
        thorny_guild = await nexus.ThornyGuild.build(message.guild)

        if thorny_guild.get_channel_id('logs'):
            logs_channel = thorny.get_channel(thorny_guild.get_channel_id('logs'))

            await logs_channel.send(embed=uikit.message_delete_embed(message, datetime.now()))


@thorny.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if not before.author.bot and before.content != after.content:
        thorny_guild = await nexus.ThornyGuild.build(after.guild)

        if thorny_guild.get_channel_id('logs'):
            logs_channel = thorny.get_channel(thorny_guild.get_channel_id('logs'))

            await logs_channel.send(embed=uikit.message_edit_embed(before, after, datetime.now()))


@thorny.event
async def on_member_join(member: discord.Member):
    thorny_user = await nexus.ThornyUser.build(member)
    thorny_guild = await nexus.ThornyGuild.build(member.guild)

    if thorny_guild.get_channel_id('welcome'):
        welcome_channel = thorny.get_channel(thorny_guild.get_channel_id('welcome'))

        await welcome_channel.send(embed=uikit.user_join(thorny_user, thorny_guild))


@thorny.event
async def on_member_remove(member):
    thorny_user = await nexus.ThornyUser.build(member)
    thorny_guild = await nexus.ThornyGuild.build(member.guild)

    thorny_user.active = False
    await thorny_user.update()

    if thorny_guild.get_channel_id('welcome'):
        welcome_channel = thorny.get_channel(thorny_guild.get_channel_id('welcome'))

        await welcome_channel.send(embed=uikit.user_leave(thorny_user, thorny_guild))


@thorny.event
async def on_guild_join(guild: discord.Guild):
    member_list = await guild.fetch_members().flatten()
    for member in member_list:
        await nexus.ThornyUser.build(member)

    await nexus.ThornyGuild.build(guild)


@thorny.event
async def on_guild_remove(guild: discord.Guild):
    member_list = guild.members
    for member in member_list:
        thorny_user = await nexus.ThornyUser.build(member)
        thorny_user.active = False

        await thorny_user.update()

    # await nexus.ThornyGuild.build(guild)
    # Deactivate guild here. Not implemented yet


# Load all cogs
thorny.add_cog(modules.Moderation(thorny))
thorny.add_cog(modules.Money(thorny))
thorny.add_cog(modules.Profile(thorny))
thorny.add_cog(modules.Playtime(thorny))
thorny.add_cog(modules.Level(thorny))
thorny.add_cog(modules.Leaderboard(thorny))
thorny.add_cog(modules.Other(thorny))

# Start Tasks
# birthday_checker.start()
day_counter.start()


if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(thorny.start(TOKEN))
    thorny.run(TOKEN)
