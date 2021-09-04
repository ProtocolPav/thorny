import random
from datetime import datetime

import discord
from discord.ext import commands
from activity import write_log, process_json, total_json, reset_values
from activity import profile_update
import asyncio
import json
import constants

# v1.0
# This token is for the TEST bot
TOKEN = "ODc5MjQ5MTkwODAxMjQ4Mjc2.YSM-ng.l_rYiSIvBFyuKxvgGmXefZqQR9k"
TOKEN_Thorny = "ODY3ODE1Mzk4MjA0MTEyOTE3.YPmmEg.N28SIdOPgEIyLxojDp4nHKh9MvE"
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    botactivity = discord.Activity(type=discord.ActivityType.playing,
                                   name="Everthorn lol")
    await client.change_presence(activity=botactivity)


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

        activity_channel = client.get_channel(867303669203206194)

        log_embed = discord.Embed(title=f'{ctx.author} Has Connected', colour=0x50C878)
        log_embed.add_field(name='Log in document:',
                            value=f'**CONNECT**, **{ctx.author}**, {ctx.author.id}, {current_time}')
        await activity_channel.send(embed=log_embed)

        response_embed = discord.Embed(title='You Have Connected!', color=0x50C878)
        response_embed.add_field(name=f'Activity Logged',
                                 value=f'{ctx.author.mention}, thanks for logging your activity! '
                                       f'When you leave, use **!dc** or **!disconnect**, '
                                       f'that way your leave time is also logged!\n')

        if random.randint(1, 2) == 2 or reminder_time is None:
            response_embed.add_field(name='Tip:',
                                     value=f'Thorny loves to be helpful! It can remind you to disconnect! '
                                           f'Just add a time after `!c`. It can me in `m`, `h` or even `s`!',
                                     inline=False)
        elif reminder_time is not None:
            response_embed.add_field(name='\u200b',
                                     value=f'I will remind you to disconnect in {reminder_time}',
                                     inline=False)
        response_embed.set_footer(text=f'CONNECT, {ctx.author}, {ctx.author.id}, {current_time}\nv1.0')
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
                activity_channel = client.get_channel(867303669203206194)
                current_time = datetime.now().strftime("%B %d, %Y, %H:%M:%S")
                playtime_hour = int(current_time.split(',')[2][1:3]) - int(item['time'][0:2])
                playtime_minute = int(current_time.split(',')[2][4:6]) - int(item['time'][3:5])

                log_embed = discord.Embed(title=f'{ctx.author} Has Disconnected', colour=0xE97451)
                log_embed.add_field(name='Log:',
                                    value=f'**DISCONNECT**, **{ctx.author}**, {ctx.author.id}, {current_time}')
                await activity_channel.send(embed=log_embed)

                response_embed = discord.Embed(title='You Have Disconnected!', color=0xE97451)
                response_embed.add_field(name=f'Connection marked',
                                         value=f'{ctx.author.mention}, thank you for marking down your activity! '
                                               f'Use **!c** or **!connect** to mark down connect time!'
                                               f'\nYou played for **{playtime_hour}h{playtime_minute}m**')
                response_embed.set_footer(text=f'DISCONNECT, {ctx.author}, {ctx.author.id}, {current_time}\nv1.0')
                await ctx.send(embed=response_embed)

                write_log("DISCONNECT", current_time, ctx)
                disconnected = True

                del file_list[file_list.index(item)]
                file = open('text files/temp.json', 'w')
                json.dump(file_list, file, indent=0)
                profile_update(ctx.author, playtime_hour, 'activity', 'latest_hour')
                profile_update(ctx.author, playtime_minute, 'activity', 'latest_minute')
            else:
                pass
        if not_user >= 1 and not disconnected:
            await ctx.send("You haven't connected yet!")


class Leaderboards(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx, lb_type=None, month=datetime.now().strftime("%B")):
        if lb_type == 'activity' or lb_type == 'act':
            lb_to_send = ''
            print(f'Activity gotten on {datetime.now().strftime("%B %d, %Y, %H:%M:%S")}')
            reset_values()
            process_json(month[0:3])
            total_json(month[0:3], ctx.author)
            lb_file = open(f'text files/leaderboard_{month[0:3]}21.json', 'r+')
            lb_json = json.load(lb_file)
            for rank in lb_json:
                lb_to_send = f'{lb_to_send}\n' \
                             f'**{lb_json.index(rank)+1}.** <@{rank["name"]}> • **{rank["time_played"]}h**'

            lb_embed = discord.Embed(title=f'**Activity Leaderboard {month}**',
                                     color=0x6495ED)
            lb_embed.add_field(name=f'\u200b',
                               value=f"{lb_to_send}")
            await ctx.send(embed=lb_embed)
        elif lb_type == 'money' or lb_type == 'nugs':
            await ctx.send('Coming soon...')
        else:
            await ctx.send('> **Available Leaderboards**\n\n`activity`\n`money`')


class Gateway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['gate', 'g', 'ga'])
    async def gateway(self, ctx, gatenum=None):
        send_text = ''
        if gatenum is None:
            send_text = constants.gateway_0
        elif gatenum == '1':
            send_text = constants.gateway_1
        elif gatenum == '2':
            send_text = constants.gateway_2
        elif gatenum == '3':
            send_text = constants.gateway_3
        elif gatenum == '4':
            send_text = constants.gateway_4
        await ctx.send(send_text)


class Kingdom(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['asba', 'ash', 'asb'])
    async def asbahamael(self, ctx):
        file = open('text files/kingdoms.json', 'r')
        sendtext = json.load(file)
        sendtext = f'''{sendtext[0]["slogan"]}**King**:{sendtext[0]["king"]}**Towns**:{sendtext[0]["towns"]}**Areas**:{sendtext[0]["areas"]}**Description**:
{sendtext[0]["description"]}'''
        await ctx.send(sendtext)


class Bank(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def balance(self, ctx):
        profile_update(ctx.author)
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        await ctx.send(f"Your balance is {profile[f'{ctx.author.id}']['balance']}")

    @commands.command(aliases=['amoney'])
    async def addmoney(self, ctx, amount):
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        if str(ctx.author.id) in profile:
            amount = profile[f'{ctx.author.id}']['balance'] + int(amount)
        profile_update(ctx.author, int(amount), 'balance')
        await ctx.send(f"Your balance is now {amount}")

    @commands.command(aliases=['rmoney'])
    async def removemoney(self, ctx, amount):
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        if str(ctx.author.id) in profile:
            amount = profile[f'{ctx.author.id}']['balance'] - int(amount)
        profile_update(ctx.author, int(amount), 'balance')
        await ctx.send(f"Your balance is now {amount}")

    @commands.command()
    async def pay(self, ctx, user: discord.User, amount, *reason):
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        if str(ctx.author.id) in profile:
            if profile[f'{ctx.author.id}']['balance'] - int(amount) >= 0:
                amount1 = profile[f'{ctx.author.id}']['balance'] - int(amount)
                profile_update(ctx.author, amount1, 'balance')
                amount2 = profile[f'{user.id}']['balance'] + int(amount)
                profile_update(user, amount2, 'balance')
                await ctx.send(f'{user} has received your {amount} nugs!')


@client.command()
async def profile(ctx):
    profile_update(ctx.author)
    profile = json.load(open('text files/profiles.json', 'r'))
    await ctx.send(f'''> Recent Playtime For {ctx.author}
{profile[f'{ctx.author.id}']['activity']['latest_hour']}h{
    profile[f'{ctx.author.id}']['activity']['latest_minute']}m''')


@client.command()
async def pong(ctx):
    channel = client.get_channel(620441027043524618)
    if ctx.channel == channel:
        await channel.send('pong')
    else:
        await ctx.send('This command only works in Playground!')


@client.command(aliases=['shout', 'aaa', 'scr'])
async def scream(ctx):
    screams = ['AAAaaaAaaaAAaaaAAAAAaAAaAAAAAaaAA', 'ARGHHHHHHHHHHHHHHHHHHHHhhhhhhhh', 'GAH!',
               'ROOOOoooOOOOAARRRRRRRRRR',
               '*screams*', 'https://tenor.com/view/scream-yell-mad-angry-fury-gif-3864070',
               'GASPPPPPP AAAAAAAAAAAA']
    channel = client.get_channel(620441027043524618)
    if ctx.channel == channel:
        screamnumber = random.randint(0, 5)
        await ctx.send(f'{screams[screamnumber]}\n{ctx.author.mention}, you scared me!!!')


@client.command()
async def setprefix(ctx, prefix):
    if ctx.author.id == 266202793143042048:
        client.command_prefix = prefix
        await ctx.send(f"Prefix changed to `{prefix}`")


@client.event
async def on_message(message):
    if message.content.lower() == 'hello':
        await message.channel.send("Hi!")
    elif message.content.lower() == 'pav':
        await message.channel.send('Yes. He is Pav.')
    elif message.content.lower() == '<@!879249190801248276>':
        await message.channel.send("To get help, use the `!gateway` command! It's all in there!")

    await client.process_commands(message)  # Not putting this on on_message breaks all .command()


# client.add_cog(Bank(client))
client.add_cog(Leaderboards(client))
# client.add_cog(Kingdom(client))
client.add_cog(Gateway(client))
client.add_cog(Activity(client))  # Do this for every cog. This can also be changed through commands.
client.run(TOKEN)
