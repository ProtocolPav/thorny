import discord
import random
from discord.ext import commands
import asyncio
from functions import write_log, process_json, total_json, reset_values
from functions import profile_update, activity_set
from datetime import datetime, timedelta
import json
import errors

version_file = open('./version.json', 'r+')
version = json.load(version_file)
v = version["version"]
config = json.load(open("./../thorny_data/config.json", "r"))


class Activity(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['c'], help="Log your connect time")
    async def connect(self, ctx):
        current_time = datetime.now().strftime("%B %d, %Y, %H:%M:%S")
        temp_file = open('./../thorny_data/temp.json', 'r+')
        temp_json = json.load(temp_file)

        activity_channel = self.client.get_channel(config['channels']['activity_logs'])

        log_embed = discord.Embed(title=f'CONNECTION', colour=0x009E60)
        log_embed.add_field(name='Event Log:',
                            value=f'**CONNECT**, **{ctx.author}**, '
                                  f'{ctx.author.id}, '
                                  f'{datetime.now().replace(microsecond=0)}')
        log_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await activity_channel.send(embed=log_embed)

        response_embed = discord.Embed(title="<:_plus:897823907153838121> | Ooh! You're Playing!", color=0x009E60)
        response_embed.add_field(name=f"*Keep playing... And I'll do the rest!*",
                                 value=f'{ctx.author.mention}, I am adding every single second up!\n'
                                       f"When you stop playing, use **!dc**, so I'll know when to stop "
                                       f"counting!\n\n"
                                       f"You can use **!lb act [month]** to check the *leaderboard* for any month!\n"
                                       f"And for individual activity stats, just use **!profile**!")
        response_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        for item in temp_json:
            if str(ctx.author.id) in item['userid']:
                response_embed.add_field(name=f"By the way...",
                                         value=f"You connected before, and forgot to **!dc**! "
                                               f"This happened at {item['datetime']}\n"
                                               f"But it's all good! I added **1h05m** to your playtime :))",
                                         inline=False)
                total = activity_set(ctx.author, 'total', "1:05:00")
                profile_update(ctx.author, f"{total}", 'activity', 'total')

                month_total = activity_set(ctx.author, 'current_month', "1:05:00")
                profile_update(ctx.author, f"{month_total}", 'activity', 'current_month')
                del temp_json[temp_json.index(item)]
            else:
                pass

        response_embed.set_footer(text=f'CONNECT at {datetime.now().replace(microsecond=0)} | {v}')

        await ctx.send(embed=response_embed)

        write_log("CONNECT", datetime.now().replace(microsecond=0), ctx)
        temp_json.append({"status": "CONNECT",
                          "user": f"{ctx.author}",
                          "userid": f"{ctx.author.id}",
                          "datetime": str(datetime.now().replace(microsecond=0))})

        temp_file.truncate(0)
        temp_file.seek(0)
        json.dump(temp_json, temp_file, indent=0)

    @commands.command(aliases=['dc'], help="Log your disconnect time")
    async def disconnect(self, ctx):
        temp_file = open('./../thorny_data/temp.json', 'r+')
        temp_json = json.load(temp_file)
        disconnected = False
        not_user = 0
        for item in temp_json:
            if str(ctx.author.id) not in item['userid'] and not disconnected:
                not_user += 1
            elif str(ctx.author.id) in item['userid'] and not disconnected:
                activity_channel = self.client.get_channel(config['channels']['activity_logs'])

                playtime = datetime.now().replace(microsecond=0) - \
                           datetime.strptime(item['datetime'], "%Y-%m-%d %H:%M:%S")
                if playtime > timedelta(hours=12):
                    playtime = timedelta(hours=1, minutes=5)

                log_embed = discord.Embed(title=f'DISCONNECTION', colour=0xFA5F55)
                log_embed.add_field(name='Event Log:',
                                    value=f'**DISCONNECT**, **{ctx.author}**, '
                                          f'{ctx.author.id}, {datetime.now().replace(microsecond=0)}\n'
                                          f'Playtime: **{str(playtime).split(":")[0]}h{str(playtime).split(":")[1]}m**')
                log_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await activity_channel.send(embed=log_embed)

                response_embed = discord.Embed(title="<:_minus:897823907053203457> | Hope You Had Fun!",
                                               color=0xFA5F55)
                response_embed.add_field(name=f"*You played, and here's your stats!*",
                                         value=f'{ctx.author.mention}, you played for a total of '
                                               f'**{str(playtime).split(":")[0]}h{str(playtime).split(":")[1]}m**!\n'
                                               f"Once you feel like playing again, use **!c** to connect. You know the "
                                               f"drill.\n\n"
                                               f"You can use **!lb act [month]** to check the *leaderboard* "
                                               f"for any month!\n"
                                               f"And for individual activity stats, just use **!profile**!")
                response_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                response_embed.set_footer(text=f'DISCONNECT at {datetime.now().replace(microsecond=0)} | {v}')
                await ctx.send(embed=response_embed)

                write_log("DISCONNECT", datetime.now().replace(microsecond=0), ctx)
                disconnected = True
                del temp_json[temp_json.index(item)]

                temp_file = open('./../thorny_data/temp.json', 'w')
                temp_file.truncate(0)
                temp_file.seek(0)
                json.dump(temp_json, temp_file, indent=0)

                profile_update(ctx.author)

                total = activity_set(ctx.author, 'total', str(playtime))
                profile_update(ctx.author, f"{total}", 'activity', 'total')
                month_total = activity_set(ctx.author, 'current_month', str(playtime))

                profile_update(ctx.author, f"{month_total}", 'activity', 'current_month')
                profile_update(ctx.author, f"{str(playtime).split(':')[0]}h{str(playtime).split(':')[1]}m",
                               'activity', 'latest_playtime')
            else:
                pass
        if not_user >= 1 and not disconnected:
            await ctx.send(embed=errors.Activity.connect_error)

    @commands.command(help="See all players currently connected")
    async def online(self, ctx):
        temp_file = open('./../thorny_data/temp.json', 'r+')
        send_text = ''
        for player in json.load(temp_file)[1:]:
            time = datetime.now() - datetime.strptime(player['datetime'], '%Y-%m-%d %H:%M:%S')
            send_text = f"{send_text}\n" \
                        f"<@{player['userid']}> • connected {str(time).split(':')[0]}h{str(time).split(':')[1]}m ago"

        online_embed = discord.Embed(color=0x6495ED)
        if send_text == "":
            online_embed.add_field(name="Empty!",
                                   value="The Realm is Empty! Nobody is connected!")
        else:
            online_embed.add_field(name="Current Players Online",
                                   value=send_text)

        await ctx.send(embed=online_embed)
