import discord
from discord.ext import commands
from thorny_core import dbutils, dbclass as db
from datetime import datetime, timedelta
import json
from thorny_core import errors
from thorny_core import dbevent as ev
from thorny_core.dbfactory import ThornyFactory

version_file = open('./version.json', 'r+')
version = json.load(version_file)
v = version["version"]
config = json.load(open("./../thorny_data/config.json", "r"))


class Playtime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Log your connect time")
    async def connect(self, ctx):
        thorny_user = await ThornyFactory.build(ctx.author)

        connection: ev.Event = await ev.fetch(ev.ConnectEvent, thorny_user, self.client)
        await connection.log_event_in_database()

        if connection.metadata.database_log:
            await connection.log_event_in_discord()

            response_embed = discord.Embed(title="Playing? On Everthorn?! :smile:",
                                           color=0x00FF7F)
            response_embed.add_field(name=f"**One, Two, Thirty!**",
                                     value=f"I'm adding up your seconds, so when you stop playing, use `/disconnect`")
            response_embed.add_field(name=f"**View Your Playtime:**",
                                     value="`/profile view` - See your profile\n`/online` - See who else is on!",
                                     inline=False)
            response_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            response_embed.set_footer(text=f'{v} | {connection.metadata.event_time}')
            await ctx.respond(embed=response_embed)
        else:
            raise errors.AlreadyConnectedError()

    @commands.slash_command(description="Log your disconnect time as well as what you did")
    async def disconnect(self, ctx: discord.ApplicationContext,
                         journal: discord.Option(str, "Write a journal entry. Viewable in /journal") = None):
        thorny_user = await ThornyFactory.build(ctx.author)

        connection: ev.Event = await ev.fetch(ev.DisconnectEvent, thorny_user, self.client)
        connection.edit_metadata("event_comment", journal)
        connection.edit_metadata("level_up_message", ctx)
        await connection.log_event_in_database()

        if connection.metadata.database_log:
            playtime = str(connection.metadata.playtime).split(":")
            await connection.log_event_in_discord()

            response_embed = discord.Embed(title="Nooo Don't Go So Soon! :cry:", color=0xFF5F15)
            if connection.metadata.playtime_overtime:
                stats = f'You were connected for over 12 hours, so I brought your playtime down.' \
                        f' I set it to **1h05m**.\n'
            else:
                stats = f'You played for a total of **{playtime[0]}h{playtime[1]}m** this session. Nice!\n'
            response_embed.add_field(name=f"**Here's your stats:**",
                                     value=f'{stats}')

            xp_gain: ev.Event = await ev.fetch(ev.GainXP, thorny_user, self.client, connection.metadata)
            await xp_gain.log_event_in_database()

            if xp_gain.metadata.level_up:
                await xp_gain.log_event_in_discord()
            response_embed.add_field(name=f"**Adjust Your Hours:**",
                                     value="Did you forget to disconnect for many hours? Use the `/adjust` command "
                                           "to bring your hours down!", inline=False)
            response_embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
            response_embed.set_footer(text=f'{v} | {xp_gain.metadata.event_time} | +{xp_gain.metadata.xp_gained}xp')
            await ctx.respond(embed=response_embed)
        else:
            raise errors.NotConnectedError()

    @commands.slash_command(description='Adjust your recent playtime')
    async def adjust(self, ctx, hours: discord.Option(int, "How many hours do you want to bring down?") = None,
                     minutes: discord.Option(int, "How many minutes do you want to bring down?") = None):
        thorny_user = await ThornyFactory.build(ctx.author)
        event: ev.AdjustEvent = await ev.fetch(ev.AdjustEvent, thorny_user, self.client)
        event.metadata.adjusting_hour = abs(hours)
        event.metadata.adjusting_minute = abs(minutes)
        metadata = await event.log_event_in_database()

        if metadata.database_log:
            await ctx.respond(f'Your most recent playtime has been reduced by {hours or 0}h{minutes or 0}m.')
        else:
            raise errors.AlreadyConnectedError()

    mod = discord.SlashCommandGroup("mod", "Mod-Only commands")

    @mod.command(description="Connect a user")
    @commands.has_permissions(administrator=True)
    async def con(self, ctx, user: discord.Member):
        thorny_user = await ThornyFactory.build(user)

        connection: ev.ConnectEvent = await ev.fetch(ev.ConnectEvent, thorny_user, self.client)
        metadata = await connection.log_event_in_database()

        if metadata.database_log:
            await connection.log_event_in_discord()

            response_embed = discord.Embed(title="Playing? On Everthorn?! :smile:",
                                           color=0x00FF7F)
            response_embed.add_field(name=f"**One, Two, Thirty!**",
                                     value=f"I'm adding up your seconds, so when you stop playing, use `/disconnect`")
            response_embed.add_field(name=f"**View Your Playtime:**",
                                     value="`/profile view` - See your profile\n`/online` - See who else is on!",
                                     inline=False)
            response_embed.set_author(name=user.name, icon_url=user.display_avatar.url)
            response_embed.set_footer(text=f'{metadata.event_time}')
            await ctx.respond(f"{user.mention}, you have been connected by {ctx.author}", embed=response_embed)
        else:
            raise errors.AlreadyConnectedError()

    @mod.command(description="Disconnect a user")
    @commands.has_permissions(administrator=True)
    async def dis(self, ctx, user: discord.Member):
        thorny_user = await ThornyFactory.build(user)

        connection: ev.DisconnectEvent = await ev.fetch(ev.DisconnectEvent, thorny_user, self.client)
        connection.metadata.event_comment = f"Force disconnect by {ctx.author}"
        metadata = await connection.log_event_in_database()

        if metadata.database_log:
            playtime = str(metadata.playtime).split(":")
            await connection.log_event_in_discord()

            response_embed = discord.Embed(title="Nooo Don't Go So Soon! :cry:", color=0xFF5F15)
            if metadata.playtime_overtime:
                stats = f'You were connected for over 12 hours, so I brought your playtime down.' \
                        f'I set it to **1h05m**.'
            else:
                stats = f'You played for a total of **{playtime[0]}h{playtime[1]}m** this session. Nice!'
            response_embed.add_field(name=f"**Here's your stats:**",
                                     value=f'{stats}')
            response_embed.add_field(name=f"**Adjust Your Hours:**",
                                     value="Did you forget to disconnect for many hours? Use the `/adjust` command "
                                           "to bring your hours down!\n**Example:** `/adjust 2h34m` | Brings "
                                           "it down by 2 hours and 34 minutes", inline=False)
            response_embed.set_author(name=user.name, icon_url=user.display_avatar.url)
            response_embed.set_footer(text=f'{metadata.event_time}')
            await ctx.respond(f"{user.mention}, you have been disconnected by {ctx.author}", embed=response_embed)
        else:
            raise errors.NotConnectedError()

    @mod.command(description="Adjust a user's playtime")
    @commands.has_permissions(administrator=True)
    async def adj(self, ctx, user: discord.Member,
                  hours: discord.Option(int, "Put a - if you want to add hours") = None,
                  minutes: discord.Option(int, "Put a - if you want to add minutes") = None):
        thorny_user = await ThornyFactory.build(user)
        event: ev.AdjustEvent = await ev.fetch(ev.AdjustEvent, thorny_user, self.client)
        event.metadata.adjusting_hour = hours
        event.metadata.adjusting_minute = minutes
        metadata = await event.log_event_in_database()

        if metadata.database_log:
            await ctx.respond(f'{user.mention}, your most recent playtime has been reduced by '
                              f'{hours or 0}h{minutes or 0}m.')
        else:
            raise errors.AlreadyConnectedError()

    @commands.command(description='View your journal entries and some stats')
    async def journal(self, ctx):
        await ctx.send("This command is coming very soon to Thorny!")

    @commands.slash_command(description="See connected and AFK players and how much time they played for")
    async def online(self, ctx):
        selector = dbutils.Base()
        connected = await selector.select_online(ctx.guild.id)
        online_text = ''
        afk_text = ''
        for player in connected:
            time = datetime.now() - player['connect_time']
            if time < timedelta(hours=12):
                time = str(time).split(":")
                online_text = f"{online_text}\n" \
                              f"<@{player['user_id']}> • " \
                              f"connected {time[0]}h{time[1]}m ago"
            else:
                time = str(time).split(":")
                afk_text = f"{afk_text}\n" \
                           f"<@{player['user_id']}> • " \
                           f"connected {time[0]}h{time[1]}m ago"

        online_embed = discord.Embed(color=0x6495ED)
        if online_text == "":
            online_embed.add_field(name="**Empty!**",
                                   value="The Server is Empty! Nobody is connected!")
        elif online_text != "":
            online_embed.add_field(name="**Connected Players (Connected less than 12h ago)**\n"
                                        "*Playtime: As seen here*",
                                   value=online_text)
        if afk_text != "":
            online_embed.add_field(name="**AFK Players (Connected over 12h ago)**\n"
                                        "*Playtime: Defaults to 1h05m*",
                                   value=f"{afk_text}", inline=False)

        await ctx.respond(embed=online_embed)
