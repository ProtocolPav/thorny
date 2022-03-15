import discord
from discord.ext import commands
from thorny_code import dbutils
from datetime import datetime, timedelta
import json
import errors

version_file = open('./version.json', 'r+')
version = json.load(version_file)
v = version["version"]
config = json.load(open("./../thorny_data/config.json", "r"))


class Playtime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Log your connect time")
    async def connect(self, ctx):
        last_connect = await dbutils.Activity.select_recent_connect(ctx.author.id)
        if last_connect['disconnect_time'] is not None or last_connect is None:
            log_embed = discord.Embed(title=f'CONNECTION', colour=0x00FF7F)
            log_embed.add_field(name='Event Log:',
                                value=f'**CONNECT**, **{ctx.author}**, '
                                      f'{ctx.author.id}, '
                                      f'{datetime.now().replace(microsecond=0)}')
            log_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            activity_channel = self.client.get_channel(config['channels']['activity_logs'])
            await activity_channel.send(embed=log_embed)

            response_embed = discord.Embed(title="Playing? On Everthorn?! :smile:",
                                           color=0x00FF7F)
            response_embed.add_field(name=f"**I am adding up your seconds!**",
                                     value=f"{ctx.author.mention}, when you stop playing, use `!dc` "
                                           f"so I'll know when to stop!\n\n"
                                           "`!lb activity` - View this month's activity!\n"
                                           "`!profile` - View your individual activity stats!")
            response_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            response_embed.set_footer(text=f'{v} | {datetime.now().replace(microsecond=0)}')

            await dbutils.Activity.insert_connect(ctx)
            await ctx.respond(embed=response_embed)
        elif datetime.now() - last_connect['connect_time'] > timedelta(hours=12):
            log_embed = discord.Embed(title=f'CONNECTION', colour=0x00FF7F)
            log_embed.add_field(name='Event Log:',
                                value=f'**CONNECT**, **{ctx.author}**, '
                                      f'{ctx.author.id}, '
                                      f'{datetime.now().replace(microsecond=0)}')
            log_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            activity_channel = self.client.get_channel(config['channels']['activity_logs'])
            await activity_channel.send(embed=log_embed)

            response_embed = discord.Embed(title="Playing? On Everthorn?! :smile:", color=0x00FF7F)
            response_embed.add_field(name=f"**I am adding up your seconds!**",
                                     value=f"{ctx.author.mention}, when you stop playing, use `!dc` "
                                           f"so I'll know when to stop!\n\n"
                                           "`!lb activity` - View this month's activity\n"
                                           "`!profile` - View your individual activity stats")
            response_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            response_embed.set_footer(text=f'{v} | {datetime.now().replace(microsecond=0)}')

            await dbutils.Activity.update_disconnect(ctx.author.id, last_connect['connect_time'],
                                                     timedelta(hours=1, minutes=5))
            await dbutils.Activity.insert_connect(ctx.author.id)
            await dbutils.Activity.update_user_activity(ctx)
            await ctx.respond(embed=response_embed)
        else:
            await ctx.respond(embed=errors.Activity.already_connected_error, ephemeral=True)

    @commands.slash_command(description="Log your disconnect time as well as what you did")
    async def disconnect(self, ctx):
        last_connect = await dbutils.Activity.select_recent_connect(ctx.author.id)
        if last_connect['disconnect_time'] is None:
            playtime = datetime.now().replace(microsecond=0) - last_connect['connect_time']
            overtime = False
            if playtime > timedelta(hours=12):
                overtime = True
                playtime = timedelta(hours=1, minutes=5)

            log_embed = discord.Embed(title=f'DISCONNECTION', colour=0xFF5F15)
            log_embed.add_field(name='Event Log:',
                                value=f'**DISCONNECT**, **{ctx.author}**, '
                                      f'{ctx.author.id}, {datetime.now().replace(microsecond=0)}\n'
                                      f'Playtime: **{str(playtime).split(":")[0]}h{str(playtime).split(":")[1]}m**')
            log_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            activity_channel = self.client.get_channel(config['channels']['activity_logs'])
            await activity_channel.send(embed=log_embed)

            response_embed = discord.Embed(title="Nooo Don't Go So Soon! :cry:", color=0xFF5F15)
            if overtime:
                stats = f'{ctx.author.mention}, you were connected for over 12 hours, so I brought your playtime down' \
                        f'. I set it to **{str(playtime).split(":")[0]}h{str(playtime).split(":")[1]}m**.\n'
            else:
                stats = f'{ctx.author.mention}, you played for a total of' \
                        f' **{str(playtime).split(":")[0]}h{str(playtime).split(":")[1]}m**!\n'
            response_embed.add_field(name=f"**Here's your stats:**",
                                     value=f'{stats}'
                                           f"Use `!c` to connect again next time!\n\n"
                                           "`!lb activity` - View this month's activity\n"
                                           "`!profile` - View your individual activity stats")
            response_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
            response_embed.set_footer(text=f'{v} | {datetime.now().replace(microsecond=0)}')

            await dbutils.Activity.update_disconnect(ctx.author.id, last_connect['connect_time'],
                                                     playtime)
            await dbutils.Activity.update_user_activity(ctx)
            await ctx.respond(embed=response_embed)
        elif last_connect['disconnect_time'] is not None:
            await ctx.respond(embed=errors.Activity.connect_error, ephemeral=True)

    @commands.slash_command(description='BETA Adjust your recent playtime. Format: Xh or Xm or XhXXm')
    async def adjust(self, ctx, time):
        last_connect = await dbutils.Activity.select_recent_connect(ctx.author.id)
        if last_connect['disconnect_time'] is not None and '-' not in time:
            if 'm' in time.lower() and 'h' not in time.lower():
                time_object = timedelta(minutes=int(time[0:len(time) - 1]))
            elif 'm' not in time.lower() and 'h' in time.lower():
                time_object = timedelta(hours=int(time[0:len(time) - 1]))
            elif 'm' in time.lower() and 'h' in time.lower():
                time_list = time.lower().split('h')
                time_object = timedelta(hours=time_list[0], minutes=time_list[1][0:-1])
            else:
                time_object = timedelta(days=5000)
                await ctx.send("Please use the format 0h00m, 0h, or 0m")

            if last_connect['playtime'] - time_object > timedelta(hours=0, minutes=0):
                await dbutils.Activity.update_adjust(ctx.author.id, last_connect['connect_time'],
                                                     last_connect['playtime'] - time_object)
                await dbutils.Activity.update_user_activity(ctx)
                await ctx.respond(f'Your most recent playtime has been reduced by {time}. '
                                  f'It is now **{last_connect["playtime"] - time_object}**')
            else:
                await ctx.respond(f"Sorry! You can't remove that many hours!", ephemeral=True)

    @commands.command(description='COMING SOON! View stats about your playtime!')
    async def journal(self, ctx):
        await ctx.send("This command is coming very soon to Thorny v2.0!")

    @commands.slash_command(description="See connected and AFK players and how much time they played for")
    async def online(self, ctx):
        connected = await dbutils.Activity.select_online()
        online_text = ''
        afk_text = ''
        for player in connected:
            time = datetime.now() - player['connect_time']
            if time < timedelta(hours=12):
                online_text = f"{online_text}\n" \
                              f"<@{player['user_id']}> • " \
                              f"connected {str(time).split(':')[0]}h{str(time).split(':')[1]}m ago"
            else:
                afk_text = f"{afk_text}\n" \
                           f"<@{player['user_id']}> • " \
                           f"connected {str(time).split(':')[0]}h{str(time).split(':')[1]}m ago"

        online_embed = discord.Embed(color=0x6495ED)
        if online_text == "":
            online_embed.add_field(name="**Empty!**",
                                   value="The Realm is Empty! Nobody is connected!")
        elif online_text != "":
            online_embed.add_field(name="**Connected Players (Connected less than 12h ago)**",
                                   value=online_text)
        if afk_text != "":
            online_embed.add_field(name="**AFK Players (Connected over 12h ago)**",
                                   value=f"**These people will have their playtime default to 1h05m**\n"
                                         f"{afk_text}", inline=False)

        await ctx.respond(embed=online_embed)
