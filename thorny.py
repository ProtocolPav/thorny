import random
from datetime import datetime

import discord
from discord.ext import commands
from activity_v2 import opendoc, process, totalize, resetValues

TOKEN = "ODY3ODE1Mzk4MjA0MTEyOTE3.YPmmEg.xynVwfbP8eYx57ykzoXJGOrXf-M"
client = commands.Bot(command_prefix='!')
screams = ['AAAaaaAaaaAAaaaAAAAAaAAaAAAAAaaAA', 'ARGHHHHHHHHHHHHHHHHHHHHhhhhhhhh', 'GAH!', 'ROOOOoooOOOOAARRRRRRRRRR',
           '*screams*',
           'https://tenor.com/view/scream-yell-mad-angry-fury-gif-3864070']

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    botactivity = discord.Activity(type=discord.ActivityType.playing,
                                   name="Everthorn, of course!",
                                   large_image_url='https://everthorn.fandom.com/wiki/Special:NewFiles?file=Site-logo.png')
    await client.change_presence(activity=botactivity)


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
async def activity(ctx, month):
    temp = ''''''
    print(f'Activity gotten on {datetime.now().strftime("%B %d, %Y, %H:%M:%S")}')
    opendoc(month[0:3])
    process()
    totalize(month[0:3])
    file = open(f'processed_{month[0:3]}21.txt', 'r')
    for line in file:
        temp = f'''{temp}{line}'''
    resetValues()
    await ctx.send(f'**ACTIVITY FOR {month.upper()}**\n`{temp}`')


@client.command(aliases=['link', 'c'])
async def connect(ctx):
    activity_channel = client.get_channel(867303669203206194)
    current_time = datetime.now().strftime("%B %d, %Y, %H:%M:%S")

    await ctx.send(f'**CONNECT**, {current_time}, **{ctx.author}**,')
    await ctx.send(f'''**BETA**\n\n> {ctx.author.mention}, thank you for marking down your activity! 
> Use `!dc` to mark your leave time!''')

    #WriteFile = open(f'activity_{current_time[0:3].lower()}21.txt', 'a')
    #WriteFile.write(f'CONNECT, {current_time}, {ctx.author}, {ctx.author.id},\n')


@client.command(aliases=['unlink', 'dc'])
async def disconnect(ctx):
    activity_channel = client.get_channel(867303669203206194)
    current_time = datetime.now().strftime("%B %d, %Y, %H:%M:%S")

    await ctx.send(f'**DISCONNECT**, {current_time}, **{ctx.author}**, ||{ctx.author.id}||')
    await ctx.send(f'''**BETA**\n\n> {ctx.author.mention}, thank you for marking down your activity! 
> Use `!c` to mark your join time!''')

    #WriteFile = open(f'activity_{current_time[0:3].lower()}21.txt', 'a')
    #WriteFile.write(f'DISCONNECT, {current_time}, {ctx.author}, {ctx.author.id},\n')


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


client.run(TOKEN)
