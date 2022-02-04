import random
from datetime import datetime, timedelta
import discord
from discord.ext import commands, pages
import json
import math

from functions import write_log, process_json, total_json, reset_values
from functions import profile_update
from modules import help
import dbutils
import errors


class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pages = []

    leaderboard = discord.SlashCommandGroup("lb", "Leaderboard Commands")

    @leaderboard.command(aliases=['act'], help="See the Activity leaderboard", usage='[month] [page]')
    async def activity(self, ctx, month=None):
        self.pages = []
        if month is None:
            month = datetime.now()
        elif len(month) >= 3:
            month = datetime.strptime(month[0:3], "%b").replace(year=datetime.now().year)

        playtime = await dbutils.Leaderboard.select_activity(month)
        total_pages = math.ceil(len(playtime) / 20)
        for page in range(1, total_pages+1):
            start = page*20 - 20
            stop = page*20
            playtime_text = []
            for user in playtime[start:stop]:
                time = f"{user['sum']}"
                playtime_text.append(f'**{playtime.index(user) + 1}.** <@{user["user_id"]}> • '
                                     f'**{time.split(":")[0]}h{time.split(":")[1]}m**')
            if page != total_pages+1:
                lb_embed = discord.Embed(title=f'**{datetime.strftime(month, "%B")} Activity**',
                                         color=0x6495ED)
                lb_embed.add_field(name=f'\u200b',
                                   value='\n'.join(playtime_text), inline=False)
                lb_embed.set_footer(text=f'Page {page}/{total_pages} | Hidden Message OOooOOoOO')
                self.pages.append(lb_embed)
        paginator = pages.Paginator(pages=self.pages, timeout=30.0)
        await paginator.respond(ctx.interaction)

    @leaderboard.command(aliases=['tres'], help="See the Treasury Leaderboard")
    async def treasury(self, ctx):
        kingdom_file = open('./../thorny_data/kingdoms.json', 'r')
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
        await ctx.respond(embed=lb_embed)

    @leaderboard.command(help="See the Nugs Leaderboard", usage='[page]')
    async def nugs(self, ctx):
        self.pages = []
        balances = await dbutils.Leaderboard.select_nugs()
        total_pages = math.ceil(len(balances) / 10)
        for page in range(1, total_pages + 1):
            start = page * 10 - 10
            stop = page * 10
            balance_text = []
            for user in balances[start:stop]:
                balance_text.append(f'**{balances.index(user) + 1}.** <@{user["user_id"]}> • '
                                    f'<:Nug:884320353202081833> **{user["balance"]}**')
            if page != total_pages + 1:
                lb_embed = discord.Embed(title=f'**Nugs Leaderboard**', color=0x6495ED)
                lb_embed.add_field(name=f'\u200b',
                                   value='\n'.join(balance_text))
                lb_embed.set_footer(text=f'Page {page}/{total_pages} | Hidden Message OOooOOoOO')
                self.pages.append(lb_embed)
        paginator = pages.Paginator(pages=self.pages, timeout=30.0)
        await paginator.respond(ctx.interaction)
