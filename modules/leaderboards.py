from datetime import datetime, timedelta
import discord
from discord.ext import commands, pages
from discord.utils import basic_autocomplete
import math

from thorny_core import nexus, thorny_errors
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
                                                        default='current')):
        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)
        if not thorny_guild.has_feature('everthorn'): raise thorny_errors.AccessDenied('everthorn')

        if month == 'current':
            month = uikit.current_month()

        self.pages = []
        month = datetime.strptime(month, "%B").replace(year=datetime.now().year).date()

        thorny_user = await nexus.ThornyUser.build(ctx.author)

        playtime = await thorny_guild.get_playtime_leaderboard(month)

        rank_text = f"You are not yet on the Leaderboard"

        total_pages = math.ceil(len(playtime) / 10)
        all_texts = []
        for page in range(1, total_pages + 1):
            start = page * 10 - 10
            stop = page * 10
            playtime_text = []
            for user in playtime[start:stop]:
                time = f'{timedelta(seconds=user["value"])}'.split(':')
                playtime_text.append(f'**{playtime.index(user) + 1}.** <@{user["discord_id"]}> • '
                                     f'**{time[0]}h{time[1]}m**')

                if user['thorny_id'] == thorny_user.thorny_id:
                    rank_text = f"You are #{playtime.index(user) + 1} on the Leaderboard"

            if page != total_pages + 1:
                all_texts.append(playtime_text)

        for text in all_texts:
            lb_embed = discord.Embed(title=f'**{datetime.strftime(month, "%B")} Activity Leaderboard**',
                                     color=0x6495ED)
            lb_embed.add_field(name=f'**{rank_text}**',
                               value='\n'.join(text), inline=False)
            lb_embed.set_footer(text=f'Page {all_texts.index(text) + 1}/{total_pages}')
            self.pages.append(lb_embed)

        if not self.pages:
            raise thorny_errors.UnexpectedError2("Nobody has played yet this month!!")

        paginator = pages.Paginator(pages=self.pages, timeout=30.0)
        await paginator.respond(ctx.interaction)

    @leaderboard.command(description="See the Money Leaderboard")
    async def money(self, ctx):
        raise thorny_errors.UnexpectedError2("This command is disabled for now :((")

    @leaderboard.command(description="See the levels leaderboard")
    async def levels(self, ctx):
        raise thorny_errors.UnexpectedError2("This command is disabled for now :((")
