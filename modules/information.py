import json
import random

import discord
from discord.ext import commands
from thorny_core import dbutils
from thorny_core.dbfactory import ThornyFactory
from discord import utils


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    k_list = ["Ambria", "Asbahamael", "Dalvasha", "Eireann", "Stregabor"]
    edit_list = ["ruler_name", "capital", "alliances", "town_count", "slogan", "border_type",
                 "gov_type", "description", "lore"]

    @commands.slash_command(description="Shows the kingdom description for the kingdom")
    async def kingdom(self, ctx,
                      kingdom: discord.Option(str, "Pick a kingdom", autocomplete=utils.basic_autocomplete(k_list))):
        kingdom_record = await dbutils.Kingdom.select_kingdom(kingdom)

        kingdom_embed = discord.Embed(title=f"**{kingdom}, {kingdom_record['slogan']}**",
                                      color=0xFF5F1F)
        kingdom_embed.add_field(name=f":city_sunset: **Information**",
                                value=f"**Ruler:** {kingdom_record['ruler_name']}\n"
                                      f"**Capital City:** {kingdom_record['capital']}\n"
                                      f"**Towns:** {kingdom_record['town_count']}\n\n"
                                      f"**Kingdom Borders:** {kingdom_record['border_type']}\n"
                                      f"**Government:** {kingdom_record['gov_type']}\n"
                                      f"**Alliances:** {kingdom_record['alliances']}")
        kingdom_embed.add_field(name=f":bar_chart: **Statistics**",
                                value=f"**Kingdom Treasury:** <:Nug:884320353202081833>{kingdom_record['treasury']}\n"
                                      f"**Citizen Balances:** Coming Soon...\n"
                                      f"**Kingdom Activity:** Coming Soon...\n"
                                      f"**Members:** Coming Soon...\n"
                                      f"**Started On:** {kingdom_record['creation_date']}")
        kingdom_embed.add_field(name=f"**Kingdom Wiki Page**",
                                value=f"https://everthorn.fandom.com/wiki/{kingdom}",
                                inline=False)
        kingdom_embed.add_field(name=":scroll: **Description**",
                                value=f"{kingdom_record['description']}",
                                inline=False)
        kingdom_embed.add_field(name=":postal_horn: **Kingdom Lore**",
                                value=f"{kingdom_record['lore']}",
                                inline=False)

        await ctx.respond(embed=kingdom_embed)

    @commands.slash_command(description="Ruler Only | Edit what your Kingdom Command says")
    @commands.has_role('Ruler')
    async def kedit(self, ctx, field: discord.Option(str, autocomplete=utils.basic_autocomplete(edit_list)), value):
        thorny_user = await ThornyFactory.build(ctx.author)
        selector = dbutils.Base()
        kingdom = await selector.select('kingdom', 'user', 'thorny_user_id', thorny_user.id)

        update = await dbutils.Kingdom.update_kingdom(kingdom[0][0], field, value)
        if update == "length_error":
            await ctx.respond("This is too long!")
        else:
            await ctx.respond(f"Success! {field} is now {value} for {kingdom[0][0]}")

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
    async def gtsearch(self, ctx, gamertag: discord.Option(str, "Enter parts of a gamertag")):
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

    @commands.slash_command(description="See all current events and attendees")
    async def events(self, ctx):
        events = ctx.guild.scheduled_events
        events_embed = discord.Embed(colour=0xa35de)
        for item in events:
            print(item)
            events_embed.add_field(name=f"**{item.name}**",
                                   value=f"'*{item.description}*'\n"
                                         f"Starts on: {item.start_time}\n"
                                         f"[Click Here To Reserve A Space](www.google.com)", inline=False)
        await ctx.respond(embed=events_embed)
