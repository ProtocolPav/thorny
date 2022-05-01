import discord
from discord.ext import commands
import json
from thorny_core import errors
import random

config_file = open('./../thorny_data/config.json', 'r')
config = json.load(config_file)


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def scream(self, ctx):
        api_response = api_instance.gifs_search_get(token, "scream", limit=20)
        gifs_list = list(api_response.data)
        send_gif = random.choice(gifs_list)
        await ctx.send(f'{send_gif.embed_url}\n{ctx.author.mention}, you scared me!!!')

    @commands.command()
    async def hug(self, ctx):
        api_response = api_instance.gifs_search_get(token, "hug", limit=20)
        gifs_list = list(api_response.data)
        send_gif = random.choice(gifs_list)
        await ctx.send(f'{send_gif.embed_url}\n{ctx.author.mention}, heres a hug')

    @commands.command()
    async def slap(self, ctx):
        api_response = api_instance.gifs_search_get(token, "slap", limit=20)
        gifs_list = list(api_response.data)
        send_gif = random.choice(gifs_list)
        await ctx.send(f'{send_gif.embed_url}\n{ctx.author.mention}, you knobhead')

    @commands.command()
    async def meme(self, ctx):
        api_response = api_instance.gifs_search_get(token, "meme", limit=20)
        gifs_list = list(api_response.data)
        send_gif = random.choice(gifs_list)
        await ctx.send(f'{send_gif.embed_url}\n{ctx.author.mention}, lol')


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def game(self):
        pass