import discord
import random
from discord.ext import commands
import asyncio
from functions import write_log, process_json, total_json, reset_values
from functions import profile_update
from datetime import datetime, timedelta
import json
config_file = open('./../thorny_data/config.json', 'r+')
config = json.load(config_file)
v = config["version"]


class Activity(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['link', 'c', 'C'])
    async def connect(self, ctx, reminder_time=None):
        current_time = datetime.now().strftime("%B %d, %Y, %H:%M:%S")
        temp_file = open('./../thorny_data/temp.json', 'r+')
        temp_logs = json.load(temp_file)

        for item in temp_logs:
            if str(ctx.author.id) in item['userid']:
                del temp_logs[temp_logs.index(item)]
                await ctx.send("You already connected before, BUT it's Ay Okay! "
                               "I marked down your previous connection as 1h5m. Always glad to help :))")
            else:
                temp_file = open('./../thorny_data/temp.json', 'w')
                pass

        activity_channel = self.client.get_channel(833298586971799622)

        log_embed = discord.Embed(title=f'{ctx.author} Has Connected', colour=0x50C878)
        log_embed.add_field(name='Event Log:',
                            value=f'**CONNECT**, **{ctx.author}**, '
                                  f'{ctx.author.id}, '
                                  f'{datetime.now().replace(microsecond=0)}')
        await activity_channel.send(embed=log_embed)

        response_embed = discord.Embed(title='You Have Connected!', color=0x50C878)
        response_embed.add_field(name=f'Activity Logged',
                                 value=f'{ctx.author.mention}, thanks for logging your activity! '
                                       f'When you leave, use **!dc** or **!disconnect**, '
                                       f'that way your leave time is also logged!\n')

        if reminder_time is None:
            response_embed.add_field(name='Tip:',
                                     value=f'Thorny loves to be helpful! It can remind you to disconnect! '
                                           f'Just add a time after `!c`. It can me in `m`, `h` or even `s`!',
                                     inline=False)
        elif reminder_time is not None:
            response_embed.add_field(name='\u200b',
                                     value=f'I will remind you to disconnect in {reminder_time}',
                                     inline=False)
        response_embed.set_footer(text=f'CONNECT at '
                                       f'{datetime.now().replace(microsecond=0)} | {v}')
        await ctx.send(embed=response_embed)

        write_log("CONNECT", datetime.now().replace(microsecond=0), ctx)
        temp_logs.append({"status": "CONNECT",
                          "user": f"{ctx.author}",
                          "userid": f"{ctx.author.id}",
                          "datetime": str(datetime.now().replace(microsecond=0))})
        json.dump(temp_logs, temp_file, indent=0)

        if reminder_time is not None:
            if 'h' in reminder_time:
                reminder_time = int(reminder_time[0:len(reminder_time) - 1]) * 60 * 60
            elif 'm' in reminder_time:
                reminder_time = int(reminder_time[0:len(reminder_time) - 1]) * 60
            elif 's' in reminder_time:
                reminder_time = int(reminder_time[0:len(reminder_time) - 1])
            await asyncio.sleep(int(reminder_time))
            await ctx.send(f'{ctx.author.mention}, '
                           f'you told me to remind you {reminder_time} seconds ago to disconnect!')

    @commands.command(aliases=['unlink', 'dc', 'Dc'])
    async def disconnect(self, ctx):
        file = open('./../thorny_data/temp.json', 'r+')
        file_list = json.load(file)
        disconnected = False
        not_user = 0
        for item in file_list:
            if str(ctx.author.id) not in item['userid'] and not disconnected:
                not_user += 1
            elif str(ctx.author.id) in item['userid'] and not disconnected:
                activity_channel = self.client.get_channel(867303669203206194)

                playtime = datetime.now().replace(microsecond=0) - \
                           datetime.strptime(item['datetime'], "%Y-%m-%d %H:%M:%S")
                if playtime > timedelta(hours=12):
                    playtime = timedelta(hours=1, minutes=5)

                log_embed = discord.Embed(title=f'{ctx.author} Has Disconnected', colour=0xE97451)
                log_embed.add_field(name='Log:',
                                    value=f'**DISCONNECT**, **{ctx.author}**, '
                                          f'{ctx.author.id}, {datetime.now().replace(microsecond=0)}\n'
                                          f'Playtime: **{playtime}**')
                await ctx.send(embed=log_embed)

                response_embed = discord.Embed(title='You Have Disconnected!', color=0xE97451)
                response_embed.add_field(name=f'Connection marked',
                                         value=f'{ctx.author.mention}, thank you for marking down your activity! '
                                               f'Use **!c** or **!connect** to mark down connect time!'
                                               f'\nYou played for **{str(playtime).split(":")[0]}h'
                                               f'{str(playtime).split(":")[1]}m**')
                response_embed.set_footer(text=f'DISCONNECT, {ctx.author}, '
                                               f'{ctx.author.id}, '
                                               f'{datetime.now().replace(microsecond=0)}\n{v}')
                await ctx.send(embed=response_embed)

                write_log("DISCONNECT", datetime.now().replace(microsecond=0), ctx)
                disconnected = True

                del file_list[file_list.index(item)]
                file = open('./../thorny_data/temp.json', 'w')
                json.dump(file_list, file, indent=0)
                file = open('./../thorny_data/profiles.json', 'r+')
                file_loaded = json.load(file)
                playtime = str(playtime)
                total = datetime.strptime(file_loaded[f'{ctx.author.id}']['activity']['total'], "%Hh%Mm") \
                        + timedelta(hours=int(playtime[0:2]), minutes=int(playtime[3:4]))
                total = datetime.strftime(total, "%Hh%Mm")
                profile_update(ctx.author, f'{total}', 'activity', 'total')
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
