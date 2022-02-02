import json

import discord
from discord.ext import commands
from modules import help
import functions
import dbutils


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="CM Only | Change the ruler within the Gateway Command", hidden=True)
    @commands.has_permissions(administrator=True)
    async def newruler(self, ctx, kingdom, *ruler):
        config['kingdoms'][f'{kingdom.lower()}']['ruler'] = f'{" ".join(ruler)}'
        json.dump(config, open('./../thorny_data/config.json', 'w'), indent=3)
        await ctx.send(f"Ruler is now {' '.join(ruler)}")

    @commands.command()
    async def new(self, ctx):
        file_new_cmd = open("./../thorny_data/new_command.txt", "r").read()
        config_file = open('./../thorny_data/config.json', 'r+')
        config = json.load(config_file)
        await ctx.send(file_new_cmd.format(config['kingdoms']['ambria']['ruler'],
                                           config['kingdoms']['asbahamael']['ruler'],
                                           config['kingdoms']['dalvasha']['ruler'],
                                           config['kingdoms']['eireann']['ruler'],
                                           config['kingdoms']['stregabor']['ruler']))

    @commands.command(help="Shows the kingdom description for the kingdom",
                      aliases=['stregabor', 'dalvasha', 'eireann', 'ambria'],
                      brief='!stregabor')
    async def asbahamael(self, ctx):
        kingdom = ctx.message.content[1:].capitalize()
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
                                value=f"Soon...",
                                inline=False)

        await ctx.send(embed=kingdom_embed)

    @commands.command(help="Ruler Only | Edit what your Kingdom Command says")
    @commands.has_role('Ruler')
    async def kedit(self, ctx, field=None, *value):
        kingdom = await dbutils.condition_select('user', 'kingdom', 'user_id', ctx.author.id)

        update = await dbutils.Kingdom.update_kingdom(kingdom[0][0], field, " ".join(value))
        if update == "length_error":
            await ctx.send("Too long of a character")
        elif update == "section_error":
            await help.Help.kingdoms(self, ctx)
        else:
            await ctx.send(f"Success! {field} is now {' '.join(value)} for {kingdom[0][0]}")

    @commands.slash_command(description="Get help on editing the Kingdom Command", guild_ids=[733716450774351933])
    async def kingdoms(self, ctx):
        help_embed = discord.Embed(colour=0x65b39b)
        help_embed.add_field(name=":question: **Kingdom Help**",
                             value=f"**!kedit <field> <value>** - Edit a certain field on the command!")
        help_embed.add_field(name=":pencil: **Fields You Can Edit**",
                             value=f"You can edit the following fields (In order from top to bottom):\n\n"
                                   f"**Slogan** - The top part of the kingdom command | Max. 5 words\n"
                                   f"**Ruler** - Your Kingdom's Ruler\n"
                                   f"**Capital** - The Capital CIty | Max. 30 characters\n"
                                   f"**Border_type** - Open, Closed, Partially Open | Max. 30 characters\n"
                                   f"**Gov_type** - Kingdom's Government Type\n"
                                   f"**Alliances** - Your kingdom's alliances | Max. 50 characters\n"
                                   f"**Description** - Your Kingdom's Description | Max. 30 words\n"
                                   f"**Lore** - Your Kingdom's Lore | Max. 30 words",
                             inline=False)
        help_embed.set_footer(text=f"Use !help kingdoms to access this!")
        await ctx.send(embed=help_embed)

    @commands.command(help="Get a random tip!")
    async def tip(self, ctx, number=None):
        tip = json.load(open('./../thorny_data/tips.json', 'r'))
        tip_embed = discord.Embed(color=0x65b39b)
        if number is None:
            number = str(random.randint(1, len(tip['tips'])))
        tip_embed.add_field(name=f"Pro Tip!",
                            value=tip['tips'][number])
        tip_embed.set_footer(text=f"Tip {number}/{len(tip['tips'])} | Use !tip [number] to get a tip!")
        await ctx.send(embed=tip_embed)

    @commands.command(aliases=["form"], help="Get a link to the EverForms")
    async def everforms(self, ctx):
        await ctx.send(f"**Here's a link!**\n"
                       f"EverForms is the unified way to submit different forms!\n"
                       f"https://forms.gle/kTaB7NN2gkpzWmcs7")
