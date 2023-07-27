import discord
from discord.ext import commands
from datetime import datetime, timedelta
import json
from thorny_core import errors
from thorny_core.db import event
from thorny_core.db import UserFactory, GuildFactory
import thorny_core.uikit as uikit
import httpx

version_file = open('./version.json', 'r+')
version = json.load(version_file)
v = version["version"]
config = json.load(open("./../thorny_data/config.json", "r"))


class Playtime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Log your connect time",
                            guild_ids=GuildFactory.get_guilds_by_feature('PLAYTIME'))
    async def connect(self, ctx):
        if ctx.guild.id == 611008530077712395:
            raise errors.AccessDenied()
        else:
            thorny_user = await UserFactory.build(ctx.author)
            thorny_guild = await GuildFactory.build(ctx.guild)

            connection = event.Connect(self.client, datetime.now(), thorny_user, thorny_guild)
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

    @commands.slash_command(description="Log your disconnect time",
                            guild_ids=GuildFactory.get_guilds_by_feature('PLAYTIME'))
    async def disconnect(self, ctx: discord.ApplicationContext):
        if ctx.guild.id == 611008530077712395:
            raise errors.AccessDenied()
        else:
            thorny_user = await UserFactory.build(ctx.author)
            thorny_guild = await GuildFactory.build(ctx.guild)

            disconnection = event.Disconnect(self.client, datetime.now(), thorny_user, thorny_guild)
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

    @commands.slash_command(description='Adjust your recent playtime',
                            guild_ids=GuildFactory.get_guilds_by_feature('PLAYTIME'))
    async def adjust(self, ctx, hours: discord.Option(int, "How many hours do you want to bring down?") = None,
                     minutes: discord.Option(int, "How many minutes do you want to bring down?") = None):
        thorny_user = await UserFactory.build(ctx.author)
        thorny_guild = await GuildFactory.build(ctx.guild)

        adjust = event.AdjustPlaytime(self.client, datetime.now(), thorny_user, thorny_guild, abs(hours or 0),
                                          abs(minutes or 0))
        await adjust.log()

        await ctx.respond(f'Your most recent playtime has been reduced by {hours or 0}h{minutes or 0}m.')

    mod = discord.SlashCommandGroup("mod", "Mod-Only commands")

    @mod.command(description="Connect a user",
                 guild_ids=GuildFactory.get_guilds_by_feature('PLAYTIME'))
    @commands.has_permissions(administrator=True)
    async def con(self, ctx, user: discord.Member):
        thorny_user = await UserFactory.build(user)
        thorny_guild = await GuildFactory.build(ctx.guild)

        connection = event.Connect(self.client, datetime.now(), thorny_user, thorny_guild)
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

    @mod.command(description="Disconnect a user",
                 guild_ids=GuildFactory.get_guilds_by_feature('PLAYTIME'))
    @commands.has_permissions(administrator=True)
    async def dis(self, ctx, user: discord.Member):
        thorny_user = await UserFactory.build(user)
        thorny_guild = await GuildFactory.build(ctx.guild)

        disconnection = event.Disconnect(self.client, datetime.now(), thorny_user, thorny_guild)
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


    @mod.command(description="Adjust a user's playtime",
                 guild_ids=GuildFactory.get_guilds_by_feature('PLAYTIME'))
    @commands.has_permissions(administrator=True)
    async def adj(self, ctx, user: discord.Member,
                  hours: discord.Option(int, "Put a - if you want to add hours") = None,
                  minutes: discord.Option(int, "Put a - if you want to add minutes") = None):
        thorny_user = await UserFactory.build(user)
        thorny_guild = await GuildFactory.build(ctx.guild)

        adjust = event.AdjustPlaytime(self.client, datetime.now(), thorny_user, thorny_guild, abs(hours), abs(minutes))
        await adjust.log()

        await ctx.respond(f'{thorny_user.discord_member.mention}, your most recent playtime has been reduced by '
                          f'{hours or 0}h{minutes or 0}m.')

    @commands.slash_command(description="See connected players and how much time they've been on for",
                            guild_ids=GuildFactory.get_guilds_by_feature('PLAYTIME'))
    async def online(self, ctx):
        thorny_guild = await GuildFactory.build(ctx.guild)
        connected = await thorny_guild.get_online_players()

        async with httpx.AsyncClient() as client:
            status: httpx.Response = await client.get("http://thorny-bds:8000/server/details", timeout=None)

        if 'EVERTHORN' in thorny_guild.features:
            everthorn_guild = True
        else:
            everthorn_guild = False

        await ctx.respond(embed=uikit.server_status(online=status.json()['server_online'],
                                                    status=status.json()['server_status'],
                                                    uptime=status.json()['uptime'],
                                                    load=status.json()['usage'],
                                                    online_players=connected,
                                                    everthorn_guilds=everthorn_guild))
