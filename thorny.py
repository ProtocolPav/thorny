from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks

import logs
import dbutils
import dbclass
import json
from thorny_code.modules import help, inventory, leaderboard, playtime, moderation, bank, gateway, profile

config = json.load(open('../thorny_data/config.json', 'r+'))
vers = json.load(open('version.json', 'r'))
v = vers["version"]

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
    print(f"[SERVER] Next month switch is in {timedelta(seconds=dbutils.Activity.seconds_until_next_month())}"
          f" (Date: {datetime.now() + timedelta(seconds=dbutils.Activity.seconds_until_next_month())})")

    print(dbutils.select_all_guilds(thorny))


@tasks.loop(seconds=dbutils.Activity.seconds_until_next_month())
async def update_months():
    if update_months.current_loop != 0:
        print(f"[ACTION] Beginning Month Switch (Loop {update_months.current_loop})")
        await dbutils.Activity.update_user_months()


@thorny.command()
async def port(ctx):
    version_file = open('version.json', 'r+')
    version = json.load(version_file)
    if not version['v1.6_ported']:
        await dbutils.create_thorny_database(ctx)
        await dbutils.port_user_profiles(ctx)
        await dbutils.port_activity(ctx)
        await dbutils.populate_tables(ctx)
        version['v1.6_ported'] = True
        version_file.truncate(0)
        version_file.seek(0)
        json.dump(version, version_file, indent=0)
        await ctx.send(f"All porting Complete!")


@thorny.command()
async def send(ctx):
    await dbclass.ThornyFactory.create(ctx.author.id, ctx.author.guild.id)
    user = await dbclass.ThornyFactory.build(ctx.author.id, ctx.author.guild.id)
    await user.inventory.fetch_slot('role')
    await ctx.send(user)


@thorny.slash_command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def ping(ctx):
    await ctx.respond(f"I am Thorny. I'm currently on {v}! I love travelling around the world and right now I'm at "
                      f"{vers['nickname']}\n**Ping:** {round(thorny.latency, 3)}s")


@thorny.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown.")
    else:
        raise error


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
    elif 'baffl' in message.content.lower():
        await message.channel.send("Is that right?")
    elif message.content.startswith('!'):
        await message.channel.send("*Hint: Maybe this command works with a `/` prefix?*")

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
    await dbclass.ThornyFactory.create(member.id, member.guild.id)


@thorny.event
async def on_guild_join(guild):
    print(f"I joined {guild.name}")
    for member in guild.members:
        if member.bot is not True:
            await dbclass.ThornyFactory.create(member.id, member.guild.id)


update_months.start()

thorny.add_cog(bank.Bank(thorny))
thorny.add_cog(leaderboard.Leaderboard(thorny))
thorny.add_cog(inventory.Inventory(thorny))
thorny.add_cog(gateway.Information(thorny))
thorny.add_cog(profile.Profile(thorny))
thorny.add_cog(moderation.Moderation(thorny))
thorny.add_cog(playtime.Playtime(thorny))
thorny.add_cog(help.Help(thorny))  # Do this for every cog. This can also be changed through commands.
thorny.run(TOKEN)
