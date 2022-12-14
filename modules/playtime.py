import discord
from discord.ext import commands
from thorny_core import dbutils
from datetime import datetime, timedelta
import json
from thorny_core import errors
from thorny_core.db import event as new_event
from thorny_core.db import UserFactory, GuildFactory

version_file = open('./version.json', 'r+')
version = json.load(version_file)
v = version["version"]
config = json.load(open("./../thorny_data/config.json", "r"))


class Playtime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Log your connect time")
    async def connect(self, ctx):
        if ctx.guild.id == 611008530077712395:
            raise errors.AccessDenied()
        else:
            thorny_user = await UserFactory.build(ctx.author)
            thorny_guild = await GuildFactory.build(ctx.guild)

            connection = new_event.Connect(self.client, datetime.now(), thorny_user, thorny_guild)
            await connection.log()

            response_embed = discord.Embed(title="OOOH! You're playing! :smile:",
                                           color=0x00FF7F)
            response_embed.add_field(name=f"**One, Two, Thirty!**",
                                     value=f"I'm adding up your seconds, so when you stop playing, use </disconnect:1>")
            response_embed.add_field(name=f"**View Your Playtime:**",
                                     value="</profile:1> - See your profile\n</online:1> - See who else is on!",
                                     inline=False)
            response_embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
            response_embed.set_footer(text=f'{v}')
            await ctx.respond(embed=response_embed)

    @commands.slash_command(description="Log your disconnect time as well as what you did")
    async def disconnect(self, ctx: discord.ApplicationContext):
        if ctx.guild.id == 611008530077712395:
            raise errors.AccessDenied()
        else:
            thorny_user = await UserFactory.build(ctx.author)
            thorny_guild = await GuildFactory.build(ctx.guild)

            disconnection = new_event.Disconnect(self.client, datetime.now(), thorny_user, thorny_guild)
            await disconnection.log()

            response_embed = discord.Embed(title="Nooo Don't Go So Soon! :cry:", color=0xFF5F15)

            if disconnection.playtime_overtime:
                stats = f'You were connected for over 12 hours, so I brought your playtime down.' \
                        f' I set it to **1h05m**.\n'
            else:
                playtime = str(disconnection.playtime).split(":")
                stats = f'You played for a total of **{playtime[0]}h{playtime[1]}m** this session. Nice!\n'

            response_embed.add_field(name=f"**Here's your stats:**",
                                     value=f'{stats}')

            response_embed.add_field(name=f"**Adjust Your Hours:**",
                                     value="Did you forget to disconnect for many hours? Use the </adjust:1> command "
                                           "to bring your hours down!", inline=False)
            response_embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
            response_embed.set_footer(text=f'{v}')
            await ctx.respond(embed=response_embed)

    @commands.slash_command(description='Adjust your recent playtime')
    async def adjust(self, ctx, hours: discord.Option(int, "How many hours do you want to bring down?") = None,
                     minutes: discord.Option(int, "How many minutes do you want to bring down?") = None):
        thorny_user = await UserFactory.build(ctx.author)
        thorny_guild = await GuildFactory.build(ctx.guild)

        adjust = new_event.AdjustPlaytime(self.client, datetime.now(), thorny_user, thorny_guild, abs(hours or 0),
                                          abs(minutes or 0))
        await adjust.log()

        await ctx.respond(f'Your most recent playtime has been reduced by {hours or 0}h{minutes or 0}m.')

    mod = discord.SlashCommandGroup("mod", "Mod-Only commands")

    @mod.command(description="Connect a user")
    @commands.has_permissions(administrator=True)
    async def con(self, ctx, user: discord.Member):
        thorny_user = await UserFactory.build(user)
        thorny_guild = await GuildFactory.build(ctx.guild)

        connection = new_event.Connect(self.client, datetime.now(), thorny_user, thorny_guild)
        await connection.log()

        response_embed = discord.Embed(title="Playing? On Everthorn?! :smile:",
                                       color=0x00FF7F)
        response_embed.add_field(name=f"**One, Two, Thirty!**",
                                 value=f"I'm adding up your seconds, so when you stop playing, use `/disconnect`")
        response_embed.add_field(name=f"**View Your Playtime:**",
                                 value="`/profile` - See your profile\n`/online` - See who else is on!",
                                 inline=False)
        response_embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        response_embed.set_footer(text=f'{v}')
        await ctx.respond(f"{user.mention}, you have been connected by {ctx.author}", embed=response_embed)

    @mod.command(description="Disconnect a user")
    @commands.has_permissions(administrator=True)
    async def dis(self, ctx, user: discord.Member):
        thorny_user = await UserFactory.build(ctx.author)
        thorny_guild = await GuildFactory.build(ctx.guild)

        disconnection = new_event.Disconnect(self.client, datetime.now(), thorny_user, thorny_guild)
        await disconnection.log()

        response_embed = discord.Embed(title="Nooo Don't Go So Soon! :cry:", color=0xFF5F15)

        if disconnection.playtime_overtime:
            stats = f'You were connected for over 12 hours, so I brought your playtime down.' \
                    f' I set it to **1h05m**.\n'
        else:
            playtime = str(disconnection.playtime).split(":")
            stats = f'You played for a total of **{playtime[0]}h{playtime[1]}m** this session. Nice!\n'

        response_embed.add_field(name=f"**Here's your stats:**",
                                 value=f'{stats}')

        response_embed.add_field(name=f"**Adjust Your Hours:**",
                                 value="Did you forget to disconnect for many hours? Use the </adjust:1> command "
                                       "to bring your hours down!", inline=False)
        response_embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
        response_embed.set_footer(text=f'{v}')
        await ctx.respond(f"{user.mention}, you have been disconnected by {ctx.author}", embed=response_embed)


    @mod.command(description="Adjust a user's playtime")
    @commands.has_permissions(administrator=True)
    async def adj(self, ctx, user: discord.Member,
                  hours: discord.Option(int, "Put a - if you want to add hours") = None,
                  minutes: discord.Option(int, "Put a - if you want to add minutes") = None):
        thorny_user = await UserFactory.build(ctx.author)
        thorny_guild = await GuildFactory.build(ctx.guild)

        adjust = new_event.AdjustPlaytime(self.client, datetime.now(), thorny_user, thorny_guild, abs(hours), abs(minutes))
        await adjust.log()

        await ctx.respond(f'{thorny_user.discord_member.mention}, your most recent playtime has been reduced by '
                          f'{hours or 0}h{minutes or 0}m.')

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
        if ctx.guild.id == 611008530077712395:
            days_since_start = datetime.now() - datetime.strptime("2022-07-30 16:00", "%Y-%m-%d %H:%M")
            online_embed.title = f"Day {days_since_start.days + 1}"
        if online_text == "":
            online_embed.add_field(name="**Empty!**",
                                   value="*All you can hear are the sounds of the crickets chirping in the silent "
                                         "night...*", inline=False)
        elif online_text != "":
            online_embed.add_field(name="**Connected Players**\n",
                                   value=online_text, inline=False)
        if afk_text != "":
            online_embed.add_field(name="**AFK Players (Connected over 12h ago)**\n"
                                        "*Playtime: Defaults to 1h05m*",
                                   value=f"{afk_text}", inline=False)

        await ctx.respond(embed=online_embed)
