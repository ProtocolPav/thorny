import json
import random

import discord
from discord.ext import commands
from thorny_core import dbutils


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="Get a random tip")
    async def tip(self, ctx, number=None):
        tip = json.load(open('./../thorny_data/tips.json', 'r'))
        tip_embed = discord.Embed(color=0x65b39b)
        if number is None:
            number = str(random.randint(1, len(tip['tips'])))
        tip_embed.add_field(name=f"Pro Tip!",
                            value=tip['tips'][number])
        tip_embed.set_footer(text=f"Tip {number}/{len(tip['tips'])} | Use /tip to get a tip!")
        await ctx.respond(embed=tip_embed)

    @commands.slash_command(description="Search the database for gamertags")
    async def gamertag(self, ctx, gamertag: discord.Option(str, "Enter parts of a gamertag")):
        selector = dbutils.Base()
        gamertags = await selector.select_gamertags(ctx.guild.id, gamertag)
        send_text = []
        for tag in gamertags:
            send_text.append(f"<@{tag['user_id']}> • {tag['gamertag']}")
        if not send_text:
            send_text.append("No matches found!")

        gamertag_embed = discord.Embed(colour=0x64d5ac)
        gamertag_embed.add_field(name=f"**Gamertags matching `{gamertag}`:**",
                                 value="\n".join(send_text))
        await ctx.respond(embed=gamertag_embed)

    # @commands.slash_command(description="See all upcoming birthdays!")
    # async def birthdays(self, ctx):
    #     list = await dbutils.User().select_birthdays()
    #     birthdays = []
    #     for user in list:
    #         if user["guild_id"] == ctx.guild.id:
    #
    #     await ctx.respond(embed=events_embed)
