import math
from datetime import date, datetime

import discord
from discord.ext import commands, pages
import json
import thorny_errors
import uikit
import nexus
import utils

version_json = json.load(open('./version.json', 'r'))
v = version_json["version"]


class Profile(commands.Cog):
    def __init__(self, client):
        self.client: discord.Client = client

    @commands.slash_command(description="See your or a user's profile")
    async def profile(self, ctx: discord.ApplicationContext,
                      user: discord.Option(discord.Member, "See someone's profile. Leave blank to see yours.",
                                           default=None)):
        await ctx.defer()

        thorny_guild = await nexus.ThornyGuild.build(ctx.guild)

        if not thorny_guild.has_feature('profile'): raise thorny_errors.AccessDenied

        if user is None:
            user = ctx.author
        thorny_user = await nexus.ThornyUser.build(user)

        pages = [await uikit.profile_main_embed(thorny_user, thorny_guild),
                 await uikit.profile_lore_embed(thorny_user),
                 await uikit.profile_stats_embed(thorny_user)
                 ]

        await ctx.respond(embed=pages[0], view=uikit.Profile(thorny_user, pages, ctx))

    gamertag = discord.SlashCommandGroup("gamertag", "Gamertag commands")

    @gamertag.command(description="Search the database for gamertags")
    async def search(self, ctx: discord.ApplicationContext, gamertag: discord.Option(str, "Enter parts of a gamertag")):
        raise thorny_errors.UnexpectedError2("This command is disabled for now :((")

    @commands.slash_command(description="See all upcoming birthdays!")
    async def birthdays(self, ctx: discord.ApplicationContext):
        all_pages = []
        birthday_users: list[nexus.ThornyUser] = []

        for member in ctx.guild.members:
            if not member.bot:
                thorny_user = await nexus.ThornyUser.build(member)

                if thorny_user.birthday:
                    birthday = thorny_user.birthday.replace(year=datetime.now().year)

                    if birthday < datetime.now():
                        birthday = birthday.replace(year=datetime.now().year + 1)

                    thorny_user.birthday = birthday
                    birthday_users.append(thorny_user)

        birthday_users.sort(key=lambda x: x.birthday)

        total_pages = math.ceil(len(birthday_users) / 10)
        all_texts = []
        for page in range(1, total_pages + 1):
            start = page * 10 - 10
            stop = page * 10
            birthday_text = []
            for user in birthday_users[start:stop]:
                days_left = (user.birthday - datetime.now()).days

                birthday_text.append(f'{user.discord_member.mention} • '
                                     f'**in {days_left} day{"s" if days_left != 1 else ""}** • '
                                     f'{user.birthday.strftime("%B %d")}')

            if page != total_pages + 1:
                all_texts.append(birthday_text)

        for text in all_texts:
            lb_embed = discord.Embed(title=f'**Upcoming Birthdays!!!**',
                                     description='You can set your birthday in the `/profile`',
                                     color=0xDE3163)
            lb_embed.add_field(name=f'',
                               value='\n'.join(text), inline=False)
            lb_embed.set_footer(text=f'Page {all_texts.index(text) + 1}/{total_pages}')
            all_pages.append(lb_embed)

        if not all_pages:
            raise thorny_errors.UnexpectedError2("No Birthdays on this server :(")

        paginator = pages.Paginator(pages=all_pages, timeout=30.0)
        await paginator.respond(ctx.interaction)
