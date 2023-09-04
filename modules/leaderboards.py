from datetime import datetime
import discord
from discord.ext import commands, pages
from discord.utils import basic_autocomplete
import math

from thorny_core.db import UserFactory, GuildFactory, generator
import thorny_core.uikit as uikit


class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.pages = []

    leaderboard = discord.SlashCommandGroup("lb", "Leaderboard Commands")

    @leaderboard.command(description="See the Activity leaderboard")
    async def activity(self, ctx, month: discord.Option(str, "Pick a month to view activity for. Leave blank "
                                                             "to see the current month.",
                                                        autocomplete=basic_autocomplete(uikit.all_months()),
                                                        default=uikit.current_month())):
        thorny_guild = await GuildFactory.build(ctx.guild)
        GuildFactory.check_guild_feature(thorny_guild, 'PLAYTIME')

        self.pages = []
        month = datetime.strptime(month[0:3], "%b").replace(year=datetime.now().year)

        thorny_user = await UserFactory.build(ctx.author)

        playtime, rank = await generator.activity_leaderboard(thorny_user, month)

        total_pages = math.ceil(len(playtime) / 10)
        for page in range(1, total_pages + 1):
            start = page * 10 - 10
            stop = page * 10
            playtime_text = []
            for user in playtime[start:stop]:
                time = f"{user['sum']}".split(":")
                playtime_text.append(f'**{playtime.index(user) + 1}.** <@{user["user_id"]}> • '
                                     f'**{time[0]}h{time[1]}m**')
            rank_text = f"You are #{rank} on the Leaderboard"

            if page != total_pages + 1:
                lb_embed = discord.Embed(title=f'**{datetime.strftime(month, "%B")} Activity Leaderboard**',
                                         color=0x6495ED)
                lb_embed.add_field(name=f'**{rank_text}**',
                                   value='\n'.join(playtime_text), inline=False)
                lb_embed.set_footer(text=f'Page {page}/{total_pages}')
                self.pages.append(lb_embed)
        paginator = pages.Paginator(pages=self.pages, timeout=30.0)
        await paginator.respond(ctx.interaction)

    @leaderboard.command(description="See the Money Leaderboard")
    async def money(self, ctx):
        thorny_user = await UserFactory.build(ctx.user)
        thorny_guild = await GuildFactory.build(ctx.guild)

        self.pages = []
        balances, rank = await generator.money_leaderboard(thorny_user)

        total_pages = math.ceil(len(balances) / 10)
        for page in range(1, total_pages + 1):
            start = page * 10 - 10
            stop = page * 10
            balance_text = []
            for user in balances[start:stop]:
                balance_text.append(f'**{balances.index(user) + 1}.** <@{user["user_id"]}> • '
                                    f'{thorny_guild.currency.emoji} **{user["balance"]}**')
            rank_text = f"You are #{rank} on the Leaderboard"

            if page != total_pages + 1:
                lb_embed = discord.Embed(title=f'**{thorny_guild.currency.name.capitalize()} Leaderboard**',
                                         color=0x6495ED,
                                         description=f"**Total {thorny_guild.currency.name} in circulation:** "
                                                     f"{thorny_guild.currency.emoji} "
                                                     f"{thorny_guild.currency.total_in_circulation}")
                lb_embed.add_field(name=f'**{rank_text}**',
                                   value='\n'.join(balance_text))
                lb_embed.set_footer(text=f'Page {page}/{total_pages}')
                self.pages.append(lb_embed)
        paginator = pages.Paginator(pages=self.pages, timeout=30.0)
        await paginator.respond(ctx.interaction)

    @leaderboard.command(description="See the levels leaderboard")
    async def levels(self, ctx):
        thorny_guild = await GuildFactory.build(ctx.guild)
        GuildFactory.check_guild_feature(thorny_guild, 'LEVELS')

        self.pages = []
        thorny_user = await UserFactory.build(ctx.author)

        levels, rank = await generator.levels_leaderboard(thorny_user)

        total_pages = math.ceil(len(levels) / 10)
        for page in range(1, total_pages + 1):
            start = page * 10 - 10
            stop = page * 10
            balance_text = []
            for user in levels[start:stop]:
                balance_text.append(f'**{levels.index(user) + 1}.** <@{user["user_id"]}> • '
                                    f'**Lvl. {user["user_level"]}**')
            rank_text = f"You are #{rank} on the Leaderboard"

            if page != total_pages + 1:
                lb_embed = discord.Embed(title=f'**Levels Leaderboard**', color=0x6495ED)
                lb_embed.add_field(name=f'**{rank_text}**',
                                   value='\n'.join(balance_text))
                lb_embed.set_footer(text=f'Page {page}/{total_pages} | Level up by chatting!')
                self.pages.append(lb_embed)
        paginator = pages.Paginator(pages=self.pages, timeout=30.0)
        await paginator.respond(ctx.interaction)
