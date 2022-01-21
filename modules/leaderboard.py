import random
from datetime import datetime, timedelta
import discord
from discord.ext import commands
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

    @commands.group(aliases=['lb'], invoke_without_command=True, help="See all available leaderboards")
    async def leaderboard(self, ctx):
        await help.Help.help(self, ctx, 'Leaderboard')

    @leaderboard.command(aliases=['act'], help="See the Activity leaderboard", usage='[month] [page]')
    async def activity(self, ctx, month=None, page=1):
        if month is None:
            month = datetime.now()
        elif len(month) >= 3:
            month = datetime.strptime(month[0:3], "%b").replace(year=datetime.now().year)
        try:
            int(month)
        except TypeError or ValueError:
            start = (int(page) - 1) * 20
            stop = start + 20
            playtime = await dbutils.Leaderboard.select_activity(month)
            if start > len(playtime):
                await ctx.send(embed=errors.Leaderboard.page_error)
            else:
                playtime_text = []
                for user in playtime[start:stop]:
                    time = f"{user['sum']}"
                    playtime_text.append(f'**{playtime.index(user) + 1}.** <@{user["user_id"]}> • '
                                         f'**{time.split(":")[0]}h{time.split(":")[1]}m**')

                lb_embed = discord.Embed(title=f'**{datetime.strftime(month, "%B")} Activity**',
                                         color=0x6495ED)
                lb_embed.add_field(name=f'\u200b',
                                   value='\n'.join(playtime_text), inline=False)
                lb_embed.set_footer(
                    text=f'Page {page}/{math.ceil(len(playtime) / 20)} | Use !leaderboard to see others')
                await ctx.send(embed=lb_embed)
        else:
            await ctx.send(embed=errors.Leaderboard.month_syntax_error)

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
        await ctx.send(embed=lb_embed)

    @leaderboard.command(help="See the Nugs Leaderboard", usage='[page]')
    async def nugs(self, ctx, page=1):
        start = (int(page) - 1) * 10
        stop = start + 10
        balances = await dbutils.Leaderboard.select_nugs()
        if start > len(balances):
            await ctx.send(embed=errors.Leaderboard.page_error)
        else:
            balance_text = []
            for user in balances[start:stop]:
                balance_text.append(f'**{balances.index(user) + 1}.** <@{user["user_id"]}> • '
                                    f'<:Nug:884320353202081833> **{user["balance"]}**')

            lb_embed = discord.Embed(title=f'**Nugs Leaderboard**', color=0x6495ED)
            lb_embed.add_field(name=f'\u200b',
                               value='\n'.join(balance_text))
            lb_embed.set_footer(
                text=f'Page {page}/{math.ceil(len(balances) / 10)} | Use !leaderboard to see others')
            await ctx.send(embed=lb_embed)
