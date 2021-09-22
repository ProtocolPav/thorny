import discord
import random
from discord.ext import commands
import asyncio
from Thorny_Bot.activity import write_log, process_json, total_json, reset_values
from Thorny_Bot.activity import profile_update
from datetime import datetime
import json

class Activity(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['link', 'c', 'C'])
    async def connect(self, ctx, reminder_time=None):
        current_time = datetime.now().strftime("%B %d, %Y, %H:%M:%S")
        temp_file = open('text files/temp.json', 'r+')
        temp_logs = json.load(temp_file)

        for item in temp_logs:
            if str(ctx.author.id) in item['userid']:
                del temp_logs[temp_logs.index(item)]
                await ctx.send("You already connected before, BUT it's Ay Okay! "
                               "I marked down your previous connection as 1h5m. Always glad to help :))")
            else:
                temp_file = open('text files/temp.json', 'w')
                pass

        activity_channel = thorny.get_channel(867303669203206194)

        log_embed = discord.Embed(title=f'{ctx.author} Has Connected', colour=0x50C878)
        log_embed.add_field(name='Log in document:',
                            value=f'**CONNECT**, **{ctx.author}**, {ctx.author.id}, {current_time}')
        await activity_channel.send(embed=log_embed)

        response_embed = discord.Embed(title='You Have Connected!', color=0x50C878)
        response_embed.add_field(name=f'Activity Logged',
                                 value=f'{ctx.author.mention}, thanks for logging your Thorny_Bot! '
                                       f'When you leave, use **!dc** or **!disconnect**, '
                                       f'that way your leave time is also logged!\n')

        if random.randint(0, 2) == 2 or reminder_time is None:
            response_embed.add_field(name='Tip:',
                                     value=f'Thorny loves to be helpful! It can remind you to disconnect! '
                                           f'Just add a time after `!c`. It can me in `m`, `h` or even `s`!',
                                     inline=False)
        elif reminder_time is not None:
            response_embed.add_field(name='\u200b',
                                     value=f'I will remind you to disconnect in {reminder_time}',
                                     inline=False)
        response_embed.set_footer(text=f'CONNECT, {ctx.author}, {ctx.author.id}, {current_time}\n{v}')
        await ctx.send(embed=response_embed)

        write_log("CONNECT", current_time, ctx)
        temp_logs.append({"status": "CONNECT",
                          "user": f"{ctx.author}",
                          "userid": f"{ctx.author.id}",
                          "date": f"{current_time.split(',')[0]}",
                          "time": f"{current_time.split(',')[2][1:9]}"})
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
        file = open('text files/temp.json', 'r+')
        file_list = json.load(file)
        disconnected = False
        not_user = 0
        for item in file_list:
            if str(ctx.author.id) not in item['userid'] and not disconnected:
                not_user += 1
            elif str(ctx.author.id) in item['userid'] and not disconnected:
                activity_channel = thorny.get_channel(867303669203206194)
                current_time = datetime.now().strftime("%B %d, %Y, %H:%M:%S")
                playtime_hour = int(current_time.split(',')[2][1:3]) - int(item['time'][0:2])
                playtime_minute = int(current_time.split(',')[2][4:6]) - int(item['time'][3:5])
                if playtime_hour < 0:
                    playtime_hour += 24
                if playtime_hour >= 12:
                    playtime_hour = 2
                if playtime_minute < 0:
                    playtime_minute += 60

                log_embed = discord.Embed(title=f'{ctx.author} Has Disconnected', colour=0xE97451)
                log_embed.add_field(name='Log:',
                                    value=f'**DISCONNECT**, **{ctx.author}**, {ctx.author.id}, {current_time}\n'
                                          f'Playtime: **{playtime_hour}h{playtime_minute}m**')
                await activity_channel.send(embed=log_embed)

                response_embed = discord.Embed(title='You Have Disconnected!', color=0xE97451)
                response_embed.add_field(name=f'Connection marked',
                                         value=f'{ctx.author.mention}, thank you for marking down your Thorny_Bot! '
                                               f'Use **!c** or **!connect** to mark down connect time!'
                                               f'\nYou played for **{playtime_hour}h{playtime_minute}m**')
                response_embed.set_footer(text=f'DISCONNECT, {ctx.author}, {ctx.author.id}, {current_time}\n{v}')
                await ctx.send(embed=response_embed)

                write_log("DISCONNECT", current_time, ctx)
                disconnected = True

                del file_list[file_list.index(item)]
                file = open('text files/temp.json', 'w')
                json.dump(file_list, file, indent=0)
                file = open('text files/profiles.json', 'r+')
                file_loaded = json.load(file)
                total = file_loaded[f'{ctx.author.id}']['Thorny_Bot']['total'] + playtime_hour
                profile_update(ctx.author, total, 'Thorny_Bot', 'total')
                profile_update(ctx.author, playtime_hour, 'Thorny_Bot', 'latest_hour')
                profile_update(ctx.author, playtime_minute, 'Thorny_Bot', 'latest_minute')
            else:
                pass
        if not_user >= 1 and not disconnected:
            await ctx.send("You haven't connected yet!")

    @commands.command()
    async def online(self, ctx):
        file = open('text files/temp.json', 'r+')
        file_list = json.load(file)
        await ctx.send(file_list)