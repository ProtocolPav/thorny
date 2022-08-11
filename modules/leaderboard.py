from datetime import datetime
import discord
from discord.ext import commands, pages
import json
import math

from thorny_core import dbutils


class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pages = []

    leaderboard = discord.SlashCommandGroup("lb", "Leaderboard Commands")

    @leaderboard.command(description="See the Activity leaderboard")
    async def activity(self, ctx, month=None):
        self.pages = []
        if month is None:
            month = datetime.now()
        elif len(month) >= 3:
            month = datetime.strptime(month[0:3], "%b").replace(year=datetime.now().year)

        playtime_leaderboard = dbutils.Leaderboard()
        await playtime_leaderboard.select_activity(ctx, month)
        playtime = playtime_leaderboard.activity_list

        total_pages = math.ceil(len(playtime) / 10)
        for page in range(1, total_pages+1):
            start = page*10 - 10
            stop = page*10
            playtime_text = []
            for user in playtime[start:stop]:
                time = f"{user['sum']}".split(":")
                playtime_text.append(f'**{playtime.index(user) + 1}.** <@{user["user_id"]}> • '
                                     f'**{time[0]}h{time[1]}m**')
            rank = f"You are #{playtime_leaderboard.user_rank} on the Leaderboard"

            if page != total_pages+1:
                lb_embed = discord.Embed(title=f'**{datetime.strftime(month, "%B")} Activity Leaderboard**',
                                         color=0x6495ED)
                lb_embed.add_field(name=f'**{rank}**',
                                   value='\n'.join(playtime_text), inline=False)
                lb_embed.set_footer(text=f'Page {page}/{total_pages} | Use /connect and /disconnect')
                self.pages.append(lb_embed)
        paginator = pages.Paginator(pages=self.pages, timeout=30.0)
        await paginator.respond(ctx.interaction)

    @leaderboard.command(description="See the Treasury Leaderboard")
    async def treasury(self, ctx):
        treasury_leaderboard = dbutils.Leaderboard()
        await treasury_leaderboard.select_treasury()
        send_text = ''
        for record in treasury_leaderboard.treasury_list:
            send_text = f"{send_text}{record['kingdom']} • **<:Nug:884320353202081833>{record['treasury']}**\n"
        lb_embed = discord.Embed(title=f'**Kingdom Treasuries**',
                                 color=0x6495ED)
        lb_embed.add_field(name=f'\u200b',
                           value=f"{send_text}")
        lb_embed.set_footer(text=f'Page 1/1 | Use /treasury store to store money')
        await ctx.respond(embed=lb_embed)

    @leaderboard.command(description="See the Nugs Leaderboard")
    async def nugs(self, ctx):
        self.pages = []
        nugs_leaderboard = dbutils.Leaderboard()
        await nugs_leaderboard.select_nugs(ctx)
        balances = nugs_leaderboard.nugs_list

        total_pages = math.ceil(len(balances) / 10)
        for page in range(1, total_pages + 1):
            start = page * 10 - 10
            stop = page * 10
            balance_text = []
            for user in balances[start:stop]:
                balance_text.append(f'**{balances.index(user) + 1}.** <@{user["user_id"]}> • '
                                    f'<:Nug:884320353202081833> **{user["balance"]}**')
            rank = f"You are #{nugs_leaderboard.user_rank} on the Leaderboard"

            if page != total_pages + 1:
                lb_embed = discord.Embed(title=f'**Nugs Leaderboard**', color=0x6495ED)
                lb_embed.add_field(name=f'**{rank}**',
                                   value='\n'.join(balance_text))
                lb_embed.set_footer(text=f'Page {page}/{total_pages} | Gain Nugs by selling stuff')
                self.pages.append(lb_embed)
        paginator = pages.Paginator(pages=self.pages, timeout=30.0)
        await paginator.respond(ctx.interaction)

    @leaderboard.command(description="See the levels leaderboard")
    async def levels(self, ctx):
        self.pages = []
        levels_leaderboard = dbutils.Leaderboard()
        await levels_leaderboard.select_levels(ctx)
        levels = levels_leaderboard.levels_list

        total_pages = math.ceil(len(levels) / 10)
        for page in range(1, total_pages + 1):
            start = page * 10 - 10
            stop = page * 10
            balance_text = []
            for user in levels[start:stop]:
                balance_text.append(f'**{levels.index(user) + 1}.** <@{user["user_id"]}> • '
                                    f'**Lvl. {user["user_level"]}**')
            rank = f"You are #{levels_leaderboard.user_rank} on the Leaderboard"

            if page != total_pages + 1:
                lb_embed = discord.Embed(title=f'**Levels Leaderboard**', color=0x6495ED)
                lb_embed.add_field(name=f'**{rank}**',
                                   value='\n'.join(balance_text))
                lb_embed.set_footer(text=f'Page {page}/{total_pages} | Level up by chatting!')
                self.pages.append(lb_embed)
        paginator = pages.Paginator(pages=self.pages, timeout=30.0)
        await paginator.respond(ctx.interaction)
