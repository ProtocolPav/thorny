import random
from datetime import datetime

import discord
from discord.ext import commands
from activity import opendoc, process, totalize, resetValues
import asyncio
import json

TOKEN = "ODY3ODE1Mzk4MjA0MTEyOTE3.YPmmEg.N28SIdOPgEIyLxojDp4nHKh9MvE"
client = commands.Bot(command_prefix='!')
screams = ['AAAaaaAaaaAAaaaAAAAAaAAaAAAAAaaAA', 'ARGHHHHHHHHHHHHHHHHHHHHhhhhhhhh', 'GAH!', 'ROOOOoooOOOOAARRRRRRRRRR',
           '*screams*',
           'https://tenor.com/view/scream-yell-mad-angry-fury-gif-3864070']


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    botactivity = discord.Activity(type=discord.ActivityType.playing,
                                   name="on Everthorn. Mining away. I don't know, what to mine!")
    await client.change_presence(activity=botactivity)


class Activity(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['act'])
    async def activity(self, ctx, month):
        temp = ''''''
        print(f'Activity gotten on {datetime.now().strftime("%B %d, %Y, %H:%M:%S")}')
        opendoc(month[0:3])
        process()
        totalize(month[0:3])
        file = open(f'text files/processed_{month[0:3]}21.txt', 'r')
        for line in file:
            temp = f'''{temp}{line}'''
        resetValues()
        embed = discord.Embed(title=f'**ACTIVITY FOR {month.upper()}**', color=0xB4C424)
        embed.add_field(name=f'*Here is a list of the activity from {month} 1st*', value=f"{temp}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['link'])
    async def connect(self, ctx, remindertime=None):
        activity_channel = client.get_channel(867303669203206194)
        current_time = datetime.now().strftime("%B %d, %Y, %H:%M:%S")

        embed1 = discord.Embed(title=f'{ctx.author} Has Connected', colour=0x50C878)
        embed1.add_field(name='Log in document:',
                         value=f'**CONNECT**, {current_time}, **{ctx.author}**, ||{ctx.author.id}||')
        await ctx.send(embed=embed1)

        embed = discord.Embed(title='[BETA] You Have Connected!', color=0x50C878)
        embed.add_field(name=f'Connection marked', value=f'''
    {ctx.author.mention}, thank you for marking down your activity!
    Use **!dc** or **!disconnect** to mark down disconnect time!\n''')

        if random.randint(1, 3) == 3 and remindertime is None:
            embed.add_field(name='Tip:', value=f'''
    You can set the bot to remind you! simply type in **2h**, **20m**, or any other time you want!''', inline=False)
        embed.set_footer(text=f'CONNECT, {current_time}, {ctx.author}, {ctx.author.id}')
        await ctx.send(embed=embed)

        if remindertime is not None:
            await ctx.send(f'I will remind you in {remindertime} to disconnect!')
            if 'h' in remindertime:
                remindertime = int(remindertime[0:len(remindertime) - 1]) * 60 * 60
            elif 'm' in remindertime:
                remindertime = int(remindertime[0:len(remindertime) - 1]) * 60
            elif 's' in remindertime:
                remindertime = int(remindertime[0:len(remindertime) - 1])
            await asyncio.sleep(int(remindertime))
            await ctx.send(f'''
    {ctx.author.mention}, you told me to remind you {remindertime} seconds ago to disconnect! Make sure you did it!''')

        # WriteFile = open(f'text files/activity_{current_time[0:3].lower()}21.txt', 'a')
        # WriteFile.write(f'CONNECT, {ctx.author}, {current_time}, {ctx.author.id},\n')

    @commands.command(aliases=['unlink'])
    async def disconnect(self, ctx):
        activity_channel = client.get_channel(867303669203206194)
        current_time = datetime.now().strftime("%B %d, %Y, %H:%M:%S")

        embed1 = discord.Embed(title=f'{ctx.author} Has Disconnected', colour=0xE97451)
        embed1.add_field(name='Log in document:',
                         value=f'**DISCONNECT**, {current_time}, **{ctx.author}**, ||{ctx.author.id}||')
        await activity_channel.send(embed=embed1)

        embed = discord.Embed(title='[BETA] You Have Disconnected!', color=0xE97451)
        embed.add_field(name=f'Connection marked', value=f'''
        {ctx.author.mention}, thank you for marking down your activity!
        Use **!c** or **!connect** to mark down connect time!\n''')
        embed.set_footer(text=f'DISCONNECT, {current_time}, {ctx.author}, {ctx.author.id}')
        await ctx.send(embed=embed)

        # WriteFile = open(f'text files/activity_{current_time[0:3].lower()}21.txt', 'a')
        # WriteFile.write(f'DISCONNECT, {ctx.author}, {current_time}, {ctx.author.id},\n')


class Gateway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['gate', 'g', 'ga'])
    async def gateway(self, ctx, gatenum=None):
        sendtext = ''
        file = open('text files/gateway.json', 'r+')
        gateText = json.load(file)
        if gatenum is None:
            sendtext = f'''{gateText[0]["title"]}\n{gateText[0]["subtitle"]}\n
{gateText[0]["fields"]["command1"]}\n{gateText[0]["fields"]["command2"]}\n{gateText[0]["fields"]["command3"]}
{gateText[0]["fields"]["command4"]}'''
        elif gatenum == '1':
            sendtext = f'''{gateText[1]["title"]}\n{gateText[1]["subtitle"]}\n
{gateText[1]["fields"][f"point1"]}\n\n{gateText[1]["fields"]["point2"]}\n{gateText[1]["fields"]["king1"]}
{gateText[1]["fields"]["king2"]}\n{gateText[1]["fields"]["king3"]}\n{gateText[1]["fields"]["king4"]}
{gateText[1]["fields"]["king5"]}\n\n{gateText[1]["fields"]["point3"]}\n\n{gateText[1]["fields"]["point4"]}\n
{gateText[1]["fields"]["point5"]}'''
        elif gatenum == '2':
            sendtext = 'Coming Soon...'
        elif gatenum == '3':
            sendtext = 'Coming Soon...'
        elif gatenum == '4':
            sendtext = 'Coming Soon...'
        await ctx.send(sendtext)


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



@client.command()
async def pong(ctx):
    channel = client.get_channel(620441027043524618)
    if ctx.channel == channel:
        await channel.send('pong')
    else:
        await ctx.send('This command only works in Playground!')


@client.command(aliases=['shout', 'aaa', 'scr'])
async def scream(ctx):
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
    channel = client.get_channel(620441027043524618)
    if message.channel == channel:
        if message.content.lower() == 'hello':
            await channel.send("Hi!")

    channel2 = client.get_channel(611271483062485032)
    user1 = 266202793143042048
    if message.channel == channel2 and message.author.id != user1:
        await message.delete()

    if message.content.lower() == 'pav':
        await message.channel.send('Yes. He is Pav.')

    await client.process_commands(message)  # Not putting this on on_message breaks all .command()


client.add_cog(Kingdom(client))
client.add_cog(Gateway(client))
client.add_cog(Activity(client))  # Do this for every cog. This can also be changed through commands.
client.run(TOKEN)
