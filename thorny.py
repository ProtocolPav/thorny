import random
from datetime import datetime

import discord
from discord.ext import commands
import DiscordUtils
from activity import write_log, process_json, total_json, reset_values
from activity import profile_update
import asyncio
import json
import constants

v = 'v1.1.2'
# This token is for the TEST bot
TOKEN = "ODc5MjQ5MTkwODAxMjQ4Mjc2.YSM-ng.l_rYiSIvBFyuKxvgGmXefZqQR9k"
TOKEN_Thorny = "ODY3ODE1Mzk4MjA0MTEyOTE3.YPmmEg.N28SIdOPgEIyLxojDp4nHKh9MvE"
thorny = commands.Bot(command_prefix='!')


@thorny.event
async def on_ready():
    print(f"Logged in as {thorny.user}")
    bot_activity = discord.Activity(type=discord.ActivityType.playing,
                                   name=f"Just Guess... | {v}")
    await thorny.change_presence(activity=bot_activity)


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
                                 value=f'{ctx.author.mention}, thanks for logging your activity! '
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
                                         value=f'{ctx.author.mention}, thank you for marking down your activity! '
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
                total = file_loaded[f'{ctx.author.id}']['activity']['total'] + playtime_hour
                profile_update(ctx.author, total, 'activity', 'total')
                profile_update(ctx.author, playtime_hour, 'activity', 'latest_hour')
                profile_update(ctx.author, playtime_minute, 'activity', 'latest_minute')
            else:
                pass
        if not_user >= 1 and not disconnected:
            await ctx.send("You haven't connected yet!")


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
        await ctx.send(f'{send_text}')


class Kingdom(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['asba', 'ash', 'asb'])
    async def asbahamael(self, ctx):
        file = open('text files/kingdoms.json', 'r')
        sendtext = json.load(file)
        sendtext = f'{sendtext[0]["slogan"]}' \
                   f'**King**:{sendtext[0]["king"]}' \
                   f'**Towns**:{sendtext[0]["towns"]}' \
                   f'**Areas**:{sendtext[0]["areas"]}' \
                   f'**Description**: {sendtext[0]["description"]}'
        await ctx.send(sendtext)


class Bank(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, user: discord.User = None):
        if user is None:
            profile_update(ctx.author)
        else:
            profile_update(user)
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        if user is None:
            await ctx.send(f"Your balance is <:Nug:884320353202081833>{profile[f'{ctx.author.id}']['balance']}")
        else:
            await ctx.send(
                f"**{user.display_name}'s** balance is <:Nug:884320353202081833>{profile[f'{user.id}']['balance']}")

    @commands.command(aliases=['amoney'])
    @commands.has_permissions(administrator=True)
    async def addmoney(self, ctx, user: discord.User, amount):
        profile_update(user)
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        if str(ctx.author.id) in profile:
            amount = profile[f'{user.id}']['balance'] + int(amount)
        profile_update(user, int(amount), 'balance')
        await ctx.send(f"{user}'s balance is now {amount}")

    @commands.command(aliases=['rmoney'])
    @commands.has_permissions(administrator=True)
    async def removemoney(self, ctx, user: discord.User, amount):
        profile_update(user)
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        if str(ctx.author.id) in profile:
            amount = profile[f'{user.id}']['balance'] - int(amount)
        profile_update(user, int(amount), 'balance')
        await ctx.send(f"{user}'s balance is now {amount}")

    @commands.command()
    async def pay(self, ctx, user: discord.User, amount=None, *reason):
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        if user == ctx.author:
            error_embed = discord.Embed(color=0x900C3F)
            error_embed.add_field(name='Payment Unsuccessful!',
                                  value='Reason: You can not pay yourself silly!')
            await ctx.send(embed=error_embed)
        elif amount is None:
            error_embed = discord.Embed(color=0x900C3F)
            error_embed.add_field(name='Payment Unsuccessful!',
                                  value='Reason: You did not say an amount to pay!')
            await ctx.send(embed=error_embed)
        elif str(ctx.author.id) not in profile:
            error_embed = discord.Embed(color=0x900C3F)
            error_embed.add_field(name='Payment Unsuccessful!',
                                  value='Reason: This user is not registered in the database!')
            await ctx.send(embed=error_embed)
        elif profile[f'{ctx.author.id}']['balance'] - int(amount) < 0:
            error_embed = discord.Embed(color=0x900C3F)
            error_embed.add_field(name='Payment Unsuccessful!',
                                  value='Reason: You do not have enough nugs!')
            await ctx.send(embed=error_embed)

        elif str(ctx.author.id) in profile:
            if profile[f'{ctx.author.id}']['balance'] - int(amount) >= 0 and user != ctx.author:
                amount1 = profile[f'{ctx.author.id}']['balance'] - int(amount)
                profile_update(ctx.author, amount1, 'balance')
                amount2 = profile[f'{user.id}']['balance'] + int(amount)
                profile_update(user, amount2, 'balance')

                pay_embed = discord.Embed(color=0xDAA520)
                pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                pay_embed.add_field(name='<:Nug:884320353202081833> Payment Successful!',
                                    value=f'Amount paid: **<:Nug:884320353202081833>{amount}**\n'
                                          f'Paid to: **{user.mention}**\n'
                                          f'\n**Reason: {" ".join(str(x) for x in reason)}**')
                await ctx.send(embed=pay_embed)

    @commands.command(aliases=['tres'])
    async def treasury(self, ctx, function, amount=None):
        kingdom_file = open('text files/kingdoms.json', 'r+')
        kingdom_json = json.load(kingdom_file)
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        kingdom = ''
        if function.lower() == 'store':
            if discord.utils.find(lambda r: r.name == 'Stregabor', ctx.message.guild.roles) in ctx.author.roles:
                kingdom = 'stregabor'
            elif discord.utils.find(lambda r: r.name == 'Ambria', ctx.message.guild.roles) in ctx.author.roles:
                kingdom = 'ambria'
            elif discord.utils.find(lambda r: r.name == 'Eireann', ctx.message.guild.roles) in ctx.author.roles:
                kingdom = 'eireann'
            elif discord.utils.find(lambda r: r.name == 'Dalvasha', ctx.message.guild.roles) in ctx.author.roles:
                kingdom = 'dalvasha'
            elif discord.utils.find(lambda r: r.name == 'Asbahamael', ctx.message.guild.roles) in ctx.author.roles:
                kingdom = 'asbahamael'

            if profile[f'{ctx.author.id}']['balance'] - int(amount) >= 0:
                amount1 = profile[f'{ctx.author.id}']['balance'] - int(amount)
                profile_update(ctx.author, amount1, 'balance')
                kingdom_json[kingdom] = kingdom_json[kingdom] + int(amount)
                kingdom_file.truncate(0)
                kingdom_file.seek(0)
                json.dump(kingdom_json, kingdom_file, indent=3)

                pay_embed = discord.Embed(color=0xF88379)
                pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                pay_embed.add_field(name='<:Nug:884320353202081833> Storage Successful!',
                                    value=f'Amount stored: **<:Nug:884320353202081833>{amount}**\n'
                                          f'Stored in: **{kingdom.upper()} TREASURY**\n')
                await ctx.send(embed=pay_embed)

            elif profile[f'{ctx.author.id}']['balance'] - int(amount) < 0:
                error_embed = discord.Embed(color=0x900C3F)
                error_embed.add_field(name=f'Could not store in the {kingdom }Treasury!',
                                      value='Reason: You do not have enough nugs!')
                await ctx.send(embed=error_embed)

        elif function.lower() == 'take' and \
        discord.utils.find(lambda r: r.name == 'Ruler', ctx.message.guild.roles) in ctx.author.roles:
            if discord.utils.find(lambda r: r.name == 'Stregabor', ctx.message.guild.roles) in ctx.author.roles:
                kingdom = 'stregabor'
            elif discord.utils.find(lambda r: r.name == 'Ambria', ctx.message.guild.roles) in ctx.author.roles:
                kingdom = 'ambria'
            elif discord.utils.find(lambda r: r.name == 'Eireann', ctx.message.guild.roles) in ctx.author.roles:
                kingdom = 'eireann'
            elif discord.utils.find(lambda r: r.name == 'Dalvasha', ctx.message.guild.roles) in ctx.author.roles:
                kingdom = 'dalvasha'
            elif discord.utils.find(lambda r: r.name == 'Asbahamael', ctx.message.guild.roles) in ctx.author.roles:
                kingdom = 'asbahamael'

            if kingdom_json[kingdom] - int(amount) >= 0:
                amount1 = profile[f'{ctx.author.id}']['balance'] + int(amount)
                profile_update(ctx.author, amount1, 'balance')
                kingdom_json[kingdom] = kingdom_json[kingdom] - int(amount)
                kingdom_file.truncate(0)
                kingdom_file.seek(0)
                json.dump(kingdom_json, kingdom_file, indent=3)

                pay_embed = discord.Embed(color=0xFF7F50)
                pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                pay_embed.add_field(name='<:Nug:884320353202081833> Taking Successful!',
                                    value=f'Amount taken: **<:Nug:884320353202081833>{amount}**\n'
                                          f'Taken from: **{kingdom.upper()} TREASURY**\n')
                await ctx.send(embed=pay_embed)

            elif profile[f'{ctx.author.id}']['balance'] - int(amount) < 0:
                error_embed = discord.Embed(color=0x900C3F)
                error_embed.add_field(name=f'Could not store in the {kingdom} Treasury!',
                                      value='Reason: You do not have enough nugs!')
                await ctx.send(embed=error_embed)

        elif function.lower() == 'take' and not \
        discord.utils.find(lambda r: r.name == 'Ruler', ctx.message.guild.roles) in ctx.author.roles:
            error_embed = discord.Embed(color=0x900C3F)
            error_embed.add_field(name=f'Could not take from the Treasury!',
                                  value='Reason: You are not a Ruler!')
            await ctx.send(embed=error_embed)

        elif function.lower() == 'search':
            await Leaderboards.treasuries(self, ctx)

    @commands.command(aliases=['tpay', 'Tpay'])
    @commands.has_role('Ruler')
    async def treasury_pay(self, ctx, user: discord.User, amount=None, *reason):
        profile_file = open('text files/profiles.json', 'r+')
        profile = json.load(profile_file)
        kingdom_file = open('text files/kingdoms.json', 'r+')
        kingdom_json = json.load(kingdom_file)
        kingdom = ''

        if discord.utils.find(lambda r: r.name == 'Stregabor', ctx.message.guild.roles) in ctx.author.roles:
            kingdom = 'stregabor'
        elif discord.utils.find(lambda r: r.name == 'Ambria', ctx.message.guild.roles) in ctx.author.roles:
            kingdom = 'ambria'
        elif discord.utils.find(lambda r: r.name == 'Eireann', ctx.message.guild.roles) in ctx.author.roles:
            kingdom = 'eireann'
        elif discord.utils.find(lambda r: r.name == 'Dalvasha', ctx.message.guild.roles) in ctx.author.roles:
            kingdom = 'dalvasha'
        elif discord.utils.find(lambda r: r.name == 'Asbahamael', ctx.message.guild.roles) in ctx.author.roles:
            kingdom = 'asbahamael'

        if user == ctx.author:
            error_embed = discord.Embed(color=0x900C3F)
            error_embed.add_field(name='Payment Unsuccessful!',
                                  value='Reason: You can not pay yourself silly!')
            await ctx.send(embed=error_embed)
        elif amount is None:
            error_embed = discord.Embed(color=0x900C3F)
            error_embed.add_field(name='Payment Unsuccessful!',
                                  value='Reason: You did not say an amount to pay!')
            await ctx.send(embed=error_embed)
        elif str(ctx.author.id) not in profile:
            error_embed = discord.Embed(color=0x900C3F)
            error_embed.add_field(name='Payment Unsuccessful!',
                                  value='Reason: This user is not registered in the database!')
            await ctx.send(embed=error_embed)
        elif kingdom_json[kingdom] - int(amount) < 0:
            error_embed = discord.Embed(color=0x900C3F)
            error_embed.add_field(name='Payment Unsuccessful!',
                                  value='Reason: You do not have enough nugs!')
            await ctx.send(embed=error_embed)

        elif str(ctx.author.id) in profile:
            if kingdom_json[kingdom] - int(amount) >= 0 and user != ctx.author:
                kingdom_json[kingdom] = kingdom_json[kingdom] - int(amount)
                kingdom_file.truncate(0)
                kingdom_file.seek(0)
                json.dump(kingdom_json, kingdom_file, indent=3)

                amount2 = profile[f'{user.id}']['balance'] + int(amount)
                profile_update(user, amount2, 'balance')

                pay_embed = discord.Embed(color=0xFF7F50)
                pay_embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
                pay_embed.add_field(name='<:Nug:884320353202081833> Treasury Payment Successful!',
                                    value=f'From the **{kingdom.upper()} TREASURY**\n'
                                          f'Amount paid: **<:Nug:884320353202081833>{amount}**\n'
                                          f'Paid to: **{user.mention}**\n'
                                          f'\n**Reason: {" ".join(str(x) for x in reason)}**\n')
                await ctx.send(embed=pay_embed)


class Leaderboards(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        await ctx.send('> **Available Leaderboards**\n'
                       '\n**!activity [month] [page]** • Shows activity for all players | Also: !act'
                       "\n**!nugs [page]** • Shows a leaderboard of people's nugs | Also: !money"
                       '\n**!treasuries** • Shows the balance of all treasuries | Also: !tries'
                       '\n\n*When writing commands, do not include [the brackets]*')

    @commands.command(aliases=['act'])
    async def activity(self, ctx, month=datetime.now().strftime("%B")):
        lb_to_send = ''
        print(f'Activity gotten on {datetime.now().strftime("%B %d, %Y, %H:%M:%S")}')
        reset_values()
        process_json(month[0:3])
        total_json(month[0:3], ctx.author)
        lb_file = open(f'text files/leaderboard_{month[0:3]}21.json', 'r+')
        lb_json = json.load(lb_file)

        for rank in lb_json:
            lb_to_send = f'{lb_to_send}\n' \
                         f'**{lb_json.index(rank) + 1}.** <@{rank["name"]}> • **{rank["time_played"]}h**'

        lb_embed = discord.Embed(title=f'**Activity Leaderboard {month}**',
                                 color=0x6495ED)
        lb_embed.add_field(name=f'\u200b',
                           value=f"{lb_to_send}")
        lb_embed.set_footer(text=f'Page 1/1 | Use !leaderboard to see others')
        await ctx.send(embed=lb_embed)

    @commands.command(aliases=['money'])
    async def nugs(self, ctx, page=1):
        if page == 1:
            start = 0
            stop = 10
        else:
            start = (int(page)-1)*10
            stop = start+10

        lb_to_send = ''
        profile_file = open('text files/profiles.json', 'r')
        profile_dict = json.load(profile_file)
        profile_list = []
        for dict in profile_dict:
            profile_list.append({"user": dict, "balance": profile_dict[f"{dict}"]["balance"]})
        profile_sorted = sorted(profile_list, key=lambda x: (x["balance"]), reverse=True)[:-1]

        if start > len(profile_sorted):
            error_embed = discord.Embed(color=0x900C3F)
            error_embed.add_field(name='Woah Woah There',
                                  value='We do not have enough users to get to *that* page bro!')
            await ctx.send(embed=error_embed)
        else:
            for entry in profile_sorted[start:stop]:
                lb_to_send = f'{lb_to_send}\n' \
                             f'**{profile_sorted.index(entry) + 1}.**  <@{entry["user"]}> • ' \
                             f'<:Nug:884320353202081833>**{entry["balance"]}**'

            lb_embed = discord.Embed(title=f'**Nugs Leaderboard**',
                                     color=0x6495ED)
            lb_embed.add_field(name=f'\u200b',
                               value=f"{lb_to_send}")
            lb_embed.set_footer(text=f'Page {page}/{round(len(profile_sorted)/10)} | Use !leaderboard to see others')
            await ctx.send(embed=lb_embed)

    @commands.command(aliases=['tries'])
    async def treasuries(self, ctx):
        kingdom_file = open('text files/kingdoms.json', 'r')
        kingdom_dict = json.load(kingdom_file)
        lb_to_send = f'Ambria • **<:Nug:884320353202081833>{kingdom_dict["ambria"]}**\n' \
                     f'Asbahamael • **<:Nug:884320353202081833>{kingdom_dict["asbahamael"]}**\n' \
                     f'Eireann • **<:Nug:884320353202081833>{kingdom_dict["eireann"]}**\n' \
                     f'Dalvasha • **<:Nug:884320353202081833>{kingdom_dict["dalvasha"]}**\n' \
                     f'Stregabor • **<:Nug:884320353202081833>{kingdom_dict["stregabor"]}**\n'

        lb_embed = discord.Embed(title=f'**Kingdom Treasuries**',
                                 color=0x6495ED)
        lb_embed.add_field(name=f'\u200b',
                           value=f"{lb_to_send}")
        lb_embed.set_footer(text=f'Page 1/1 | Use !leaderboard to see others')
        await ctx.send(embed=lb_embed)


@thorny.command()
async def profile(ctx):
    profile_update(ctx.author)
    profile = json.load(open('text files/profiles.json', 'r'))
    await ctx.send(f'''> Recent Playtime For {ctx.author}
{profile[f'{ctx.author.id}']['activity']['latest_hour']}h{
    profile[f'{ctx.author.id}']['activity']['latest_minute']}m''')


@thorny.command()
async def pong(ctx):
    await ctx.send('ping!')


@thorny.command(aliases=['shout', 'aaa', 'scr'])
async def scream(ctx):
    screams = ['AAAaaaAaaaAAaaaAAAAAaAAaAAAAAaaAA', 'ARGHHHHHHHHHHHHHHHHHHHHhhhhhhhh', 'GAH!',
               'ROOOOoooOOOOAARRRRRRRRRR',
               '*screams*', 'https://tenor.com/view/scream-yell-mad-angry-fury-gif-3864070',
               'GASPPPPPP AAAAAAAAAAAA']
    screamnumber = random.randint(0, 5)
    await ctx.send(f'{screams[screamnumber]}\n{ctx.author.mention}, you scared me!!!')


@thorny.command()
async def setprefix(ctx, prefix):
    if ctx.author.id == 266202793143042048:
        thorny.command_prefix = prefix
        await ctx.send(f"Prefix changed to `{prefix}`")


@thorny.command()
async def paginate(ctx):
    embed1 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 1")
    embed2 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 2")
    embed3 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 3")
    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('🔐', "lock")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")
    embeds = [embed1, embed2, embed3]
    await paginator.run(embeds)


@thorny.event
async def on_message(message):
    if message.content.lower() == 'hello':
        await message.channel.send("Hi!")
    elif message.content.lower() == 'pav':
        await message.channel.send('Yes. He is Pav.')
    elif message.content.lower() == '<@!879249190801248276>':
        await message.channel.send('Use !gateway for help!')

    await thorny.process_commands(message)  # Not putting this on on_message breaks all .command()


@thorny.event
async def on_member_join(member):
    profile_update(member)


thorny.add_cog(Bank(thorny))
thorny.add_cog(Leaderboards(thorny))
# thorny.add_cog(Kingdom(thorny))
thorny.add_cog(Gateway(thorny))
thorny.add_cog(Activity(thorny))  # Do this for every cog. This can also be changed through commands.
thorny.run(TOKEN)
