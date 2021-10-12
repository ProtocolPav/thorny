import discord
import random
from discord.ext import commands
import asyncio
from functions import write_log, process_json, total_json, reset_values
from functions import profile_update, activity_set
from datetime import datetime, timedelta
import json

version_file = open('./version.json', 'r+')
version = json.load(version_file)
v = version["version"]


class Activity(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['link', 'c', 'C'])
    async def connect(self, ctx):
        current_time = datetime.now().strftime("%B %d, %Y, %H:%M:%S")
        temp_file = open('./../thorny_data/temp.json', 'r+')
        temp_json = json.load(temp_file)

        activity_channel = self.client.get_channel(867303669203206194)

        log_embed = discord.Embed(title=f'{ctx.author} Has Connected', colour=0x009E60)
        log_embed.add_field(name='Event Log:',
                            value=f'**CONNECT**, **{ctx.author}**, '
                                  f'{ctx.author.id}, '
                                  f'{datetime.now().replace(microsecond=0)}')
        await ctx.send(embed=log_embed)

        response_embed = discord.Embed(title="<:_like:884062799775551578> | Ooh! You're Playing!", color=0x009E60)
        response_embed.add_field(name=f"*Keep playing... And I'll do the rest!*",
                                 value=f'{ctx.author.mention}, I am adding every single second up!\n'
                                       f"When you stop playing, use **!dc**, so I'll know when to stop "
                                       f"counting!\n\n"
                                       f"You can use **!lb act <month>** to check the *leaderboard* for any month!\n"
                                       f"And for individual activity stats, just use **!profile**! Isn't "
                                       f"that just great!")
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

    @commands.command(aliases=['unlink', 'dc', 'Dc'])
    async def disconnect(self, ctx):
        temp_file = open('./../thorny_data/temp.json', 'r+')
        temp_json = json.load(temp_file)
        disconnected = False
        not_user = 0
        for item in temp_json:
            if str(ctx.author.id) not in item['userid'] and not disconnected:
                not_user += 1
            elif str(ctx.author.id) in item['userid'] and not disconnected:
                activity_channel = self.client.get_channel(867303669203206194)

                playtime = datetime.now().replace(microsecond=0) - \
                           datetime.strptime(item['datetime'], "%Y-%m-%d %H:%M:%S")
                if playtime > timedelta(hours=12):
                    playtime = timedelta(hours=1, minutes=5)

                log_embed = discord.Embed(title=f'{ctx.author} Has Disconnected', colour=0xFA5F55)
                log_embed.add_field(name='Log:',
                                    value=f'**DISCONNECT**, **{ctx.author}**, '
                                          f'{ctx.author.id}, {datetime.now().replace(microsecond=0)}\n'
                                          f'Playtime: **{playtime}**')
                await ctx.send(embed=log_embed)

                response_embed = discord.Embed(title='You Have Disconnected!', color=0xFA5F55)
                response_embed.add_field(name=f'Connection marked',
                                         value=f'{ctx.author.mention}, thank you for marking down your activity! '
                                               f'Use **!c** or **!connect** to mark down connect time!'
                                               f'\nYou played for **{str(playtime).split(":")[0]}h'
                                               f'{str(playtime).split(":")[1]}m**')
                
                response_embed.set_footer(text=f'DISCONNECT at {datetime.now().replace(microsecond=0)} | {v}')
                await ctx.send(embed=response_embed)

                write_log("DISCONNECT", datetime.now().replace(microsecond=0), ctx)
                disconnected = True

                del temp_json[temp_json.index(item)]
                temp_file = open('./../thorny_data/temp.json', 'w')
                json.dump(temp_json, temp_file, indent=0)
                total = activity_set(ctx.author, 'total', str(playtime))
                profile_update(ctx.author, f"{total}", 'activity', 'total')

                month_total = activity_set(ctx.author, 'current_month', str(playtime))
                profile_update(ctx.author, f"{month_total}", 'activity', 'current_month')
                profile_update(ctx.author, f"{str(playtime).split(':')[0]}h{str(playtime).split(':')[1]}m",
                               'activity', 'latest_playtime')
            else:
                pass
        if not_user >= 1 and not disconnected:
            await ctx.send("You haven't connected yet!")

    @commands.command()
    async def online(self, ctx):
        file = open('./../thorny_data/temp.json', 'r+')
        for player in json.load(file):
            file_list = f'\n{player}'
        await ctx.send(file_list)
